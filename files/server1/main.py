import socket
import threading
import os
from urllib.parse import unquote

HOST = '127.0.0.1'
PORT = 5698

FILE_DIR = "files"

def handleFileRequest(file_name, is_arabic=False):
    file_name = unquote(file_name.strip())
    file_path = os.path.join(FILE_DIR, file_name)

    if os.path.exists(file_path):
        if file_name.endswith((".jpg", ".png", ".jpeg")):
            content = (
                "<html lang=\"ar\" dir=\"rtl\">"
                if is_arabic
                else "<html lang=\"en\">"
            )
            return "HTTP/1.1 200 OK\r\n\r\n" + content + "\n<head><title>عرض الصورة</title></head>\n" \
                   + "<body style=\"direction: " + ('rtl' if is_arabic else 'ltr') + ";\">\n" \
                   + "<h1>" + ("ها هي الصورة المطلوبة:" if is_arabic else "Here is your requested image:") + "</h1>\n" \
                   + "<img src=\"/files/" + file_name + "\" alt=\"" + file_name + "\" style=\"max-width:100%; height:auto;\">\n" \
                   + "</body>\n</html>"
        elif file_name.endswith(".mp4"):
            return "HTTP/1.1 200 OK\r\n\r\n" \
                   + "<html lang=\"ar\" dir=\"rtl\">\n<head><title>عرض الفيديو</title></head>\n" \
                   + "<body style=\"direction: " + ('rtl' if is_arabic else 'ltr') + ";\">\n" \
                   + "<h1>" + ("ها هو الفيديو المطلوب:" if is_arabic else "Here is your requested video:") + "</h1>\n" \
                   + "<video controls style=\"max-width:100%; height:auto;\">\n" \
                   + "<source src=\"/files/" + file_name + "\" type=\"video/mp4\">\n" \
                   + ("المتصفح الخاص بك لا يدعم تشغيل الفيديو." if is_arabic else "Your browser does not support the video tag.") \
                   + "</video>\n</body>\n</html>"
        else:
            return "HTTP/1.1 400 Bad Request\r\n\r\n" + ("نوع الملف غير مدعوم!" if is_arabic else "Unsupported file type!")
    else:
        if file_name.endswith((".jpg", ".png", ".jpeg")):
            return "HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.google.com/search?q=" + file_name + "&tbm=isch\r\n\r\n"
        elif file_name.endswith(".mp4"):
            return "HTTP/1.1 307 Temporary Redirect\r\nLocation: https://www.youtube.com/results?search_query=" + file_name + "\r\n\r\n"
        else:
            return "HTTP/1.1 404 Not Found\r\n\r\n" + ("الملف المطلوب غير موجود!" if is_arabic else "File not found!")

def handleResponse(client_socket, client_address):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("Request received from " + str(client_address) + ":\n" + request)

        if "GET" in request:
            lines = request.splitlines()
            request_line = lines[0]
            parts = request_line.split(" ")

            if len(parts) < 2:
                response = "HTTP/1.1 400 Bad Request\r\n\r\nInvalid request!"
                client_socket.sendall(response.encode('utf-8'))
                return

            path = parts[1]
            if path.startswith("/request_ar_file"):
                if "?" in path:
                    query = path.split("?")[1]
                    params = query.split("&")
                    file_name = ""
                    for param in params:
                        if "=" in param:
                            key, value = param.split("=")
                            if key == "file_name":
                                file_name = value

                    if file_name:
                        response = handleFileRequest(file_name, is_arabic=True)
                        client_socket.sendall(response.encode('utf-8'))
                    else:
                        response = "HTTP/1.1 400 Bad Request\r\n\r\nالطلب غير مكتمل!"
                        client_socket.sendall(response.encode('utf-8'))
            elif path.startswith("/request_file"):
                if "?" in path:
                    query = path.split("?")[1]
                    params = query.split("&")
                    file_name = ""
                    for param in params:
                        if "=" in param:
                            key, value = param.split("=")
                            if key == "file_name":
                                file_name = value

                    if file_name:
                        response = handleFileRequest(file_name)
                        client_socket.sendall(response.encode('utf-8'))
                    else:
                        response = "HTTP/1.1 400 Bad Request\r\n\r\nMissing file_name parameter!"
                        client_socket.sendall(response.encode('utf-8'))
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nPage not found!"
                client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print("Error handling request from " + str(client_address) + ": " + str(e))
    finally:
        client_socket.close()

def start_server():
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server running on " + HOST + ":" + str(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connected by: " + str(client_address))
        threading.Thread(target=handleResponse, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
