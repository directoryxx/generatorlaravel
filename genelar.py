
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(f"{bcolors.HEADER}Generator Script Laradock")
pathNginxPath = "/Users/directoryx/Web/laradock/nginx/sites/"
pathLaravel = "~/Web/"
pathLaradock = "~/Web/laradock/"
print("Apakah yang ingin anda lakukan ?")
print("1 . Install")
print("2 . Hapus")
installLaravel = input("Perintah Anda ? ")

if installLaravel == "1":
    namaProject = input("Nama Project Laravel = ")
    laravelVer = input("Versi Laravel = ")
    print(f"{bcolors.WARNING}Memulai Installasi Laravel")
    cmd = "cd " + pathLaravel + " && composer -v create-project --prefer-dist laravel/laravel " + \
        namaProject + " \"" + laravelVer + ".*\""
    os.system(cmd)
    print(f"{bcolors.OKGREEN}Sukses Installasi Laravel")
    print("Generate Nginx Conf")

    templateconf = """
            server {

                listen 80;
                listen [::]:80;

                # For https
                # listen 443 ssl;
                # listen [::]:443 ssl ipv6only=on;
                # ssl_certificate /etc/nginx/ssl/default.crt;
                # ssl_certificate_key /etc/nginx/ssl/default.key;

                server_name """+ namaProject +""".test;
                root /var/www/"""+ namaProject +"""/public;
                index index.php index.html index.htm;

                location / {
                    try_files $uri $uri/ /index.php$is_args$args;
                }

                location ~ \.php$ {
                    try_files $uri /index.php =404;
                    fastcgi_pass php-upstream;
                    fastcgi_index index.php;
                    fastcgi_buffers 16 16k;
                    fastcgi_buffer_size 32k;
                    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                    #fixes timeouts
                    fastcgi_read_timeout 600;
                    include fastcgi_params;
                }

                location ~ /\.ht {
                    deny all;
                }

                location /.well-known/acme-challenge/ {
                    root /var/www/letsencrypt/;
                    log_not_found off;
                }

                error_log /var/log/nginx/laravel_error.log;
                access_log /var/log/nginx/laravel_access.log;
            }

    """
    fileconf = namaProject+".conf"
    print(fileconf)
    fullpath = pathNginxPath+fileconf
    print(fullpath)
    text_file = open(fullpath, "x")
    text_file.write(templateconf)
    text_file.close()
    print(f"{bcolors.WARNING}Stopping laradock")
    os.system("cd ~/Web/laradock && docker-compose down")
    print(f"{bcolors.OKGREEN}Success Stopping laradock")
    print(f"{bcolors.WARNING}Starting laradock")
    os.system("cd ~/Web/laradock && docker-compose up -d nginx mysql phpmyadmin php-fpm")
    print(f"{bcolors.OKGREEN}Success Starting laradock")

else :
    namaProject = input("Nama Project Yang akan dihapus = ")
    deletePathWeb = "rm -rf ~/Web/"+namaProject
    deletePathNginx = "rm -rf "+pathNginxPath+namaProject+".conf"
    print(f"{bcolors.WARNING}Menghapus file web")
    os.system(deletePathWeb)
    print(f"{bcolors.OKGREEN}Success Menghapus file web")
    print(f"{bcolors.WARNING}Menghapus file nginx conf")
    os.system(deletePathNginx)
    print(f"{bcolors.OKGREEN}Success Menghapus file nginx conf")

