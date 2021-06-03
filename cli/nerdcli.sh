#!/bin/sh

BASE_DIR=$(dirname "$0")

BLUE="\033[1;34m"
NC="\033[0m"

# LS can also be set to "exa" for example
LS="ls"

IP=""
PORT=""
COOKIE="$BASE_DIR/cookie.txt"

usage() {
    printf "usage: nerdcli [--parameter]\n\n"
    echo "--login                         login"
    echo "--logout                        logout"
    echo "--ls PATH                       list directory content"
    echo "--download PATH                 download file or directory"
    echo "--mkdir PATH                    make a directory"
    echo "--upload PATH FILE_PATH         upload a file"
    echo "--upload-dir PATH FILE_PATH     upload a .zip as a directory"
    echo "--delete PATH                   delete a file or directory"
    printf "\nConfig:\n\tSet IP and PORT.\n\tScript path: %s" "$BASE_DIR"
    printf "\nExamples:\n\thttps://github.com/0xHaru/Nerd-Storage/blob/master/cli/examples.md\n\n"
    printf "Project home page: https://github.com/0xHaru/Nerd-Storage\n"
}

login() {
    stty -echo
    printf "Password: "
    read -r PASSWORD
    stty echo

    login=$(curl -s -c "$COOKIE" -d password="$PASSWORD" "http://$IP:$PORT/login")
    echo "$login" | grep -q 'Incorrect password' &&
        printf "\nWrong password.\n" ||
        printf "\nLogged in.\n"
}

logout() {
    curl -s -c "$COOKIE" "http://$IP:$PORT/logout" >/dev/null && printf "Logged out.\n"
}

index() {
    (
        [ -z "$1" ] && path="index" || path="index/$1"
        html=$(curl -s -b "$COOKIE" "http://$IP:$PORT/$path")

        logged_in=$(echo "$html" | grep '/login?next=%2Findex')
        matches=$(echo "$html" | grep -E 'href="/index/|>..</a>')

        [ "$logged_in" ] && printf "You are not authenticated.\n" && exit 1

        [ -z "$matches" ] && printf "No match.\n" || {
            index=$(echo "$matches" | grep -o -P '(?<=\>)(.*?)(?=\<)')

            printf "$BLUE%s$NC\n\n" "$path"
            printf "%s\n" "$index"
        }
    )
}

download() {
    (
        path="downloads/$1"
        wget --load-cookies "$COOKIE" -q "http://$IP:$PORT/$path" && eval "$LS"
    )
}

make_dir() {
    (
        [ -z "$1" ] && path="index" || path="index/$1"
        dir="$2"
        curl -s -b "$COOKIE" -d directory="$dir" "http://$IP:$PORT/$path" >/dev/null
    )
}

upload_file() {
    (
        [ -z "$1" ] && path="index" || path="index/$1"
        file_path="$2"
        curl -s -b "$COOKIE" -F file="@$file_path" "http://$IP:$PORT/$path" >/dev/null
    )
}

upload_dir() {
    (
        [ -z "$1" ] && path="index" || path="index/$1"
        file_path="$2"
        curl -s -b "$COOKIE" -F file="@$file_path" -F dir-checkbox="True" "http://$IP:$PORT/$path" >/dev/null
    )
}

delete() {
    (
        path="index/$1"
        curl -s -b "$COOKIE" -X DELETE "http://$IP:$PORT/$path" >/dev/null
    )
}

[ "$#" -eq 0 ] && index "" || {

    while [ "$#" -gt 0 ]; do
        key="$1"

        case "$key" in
        -h | --help)
            usage
            exit 0
            ;;
        --login)
            login
            exit 0
            ;;
        --logout)
            logout
            exit 0
            ;;
        --ls)
            [ ! "$2" ] || [ "$2" = "/" ] && path="" || path="$2"
            index "$path"
            exit 0
            ;;
        --download)
            path="$2"
            download "$path"
            exit 0
            ;;
        --mkdir)
            path="$2"
            match=$(echo "$path" | grep -E '.*\/(.+)')
            [ -z "$match" ] && path="" || path=$(echo "$path" | sed 's|\(.*\)/.*|\1|')
            dir=$(echo "$2" | sed 's:.*/::')
            make_dir "$path" "$dir"
            index "$path"
            exit 0
            ;;
        --upload)
            [ ! "$3" ] && printf "Missing a parameter.\n" && exit 1
            [ "$2" = "/" ] && path="" || path="$2"
            file_path="$3"
            upload_file "$path" "$file_path"
            index "$path"
            exit 0
            ;;
        --upload-dir)
            [ ! "$3" ] && printf "Missing a parameter.\n" && exit 1
            [ "$2" = "/" ] && path="" || path="$2"
            file_path="$3"
            upload_dir "$path" "$file_path"
            index "$path"
            exit 0
            ;;
        --delete)
            path="$2"
            delete "$path"
            match=$(echo "$path" | grep -E '.*\/(.+)')
            [ -z "$match" ] && path="" || path=$(echo "$path" | sed 's|\(.*\)/.*|\1|')
            index "$path"
            exit 0
            ;;
        *)
            printf "Unknown parameter \"%s\"\n" "$key"
            usage
            exit 1
            ;;
        esac
        shift
    done
}
