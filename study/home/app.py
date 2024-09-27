from sanic import Sanic, response
from sanic.response import html

app = Sanic(__name__)

# 메인 페이지 라우트
@app.route('/')
async def index(request):
    return html('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>나의 통합 홈페이지</title>
        <style>
            :root {
                --light: #d8dbe0;
                --dark: #28292c;
                --link: rgb(27, 129, 112);
                --link-hover: rgb(24, 94, 82);
                --uiLight: rgb(200, 200, 200);
                --uiDark: rgb(50, 50, 50);
                --elseButton: rgb(120, 120, 120);
            }

            body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: var(--uiLight);
            }

            .topnav {
                overflow: hidden;
                background-color: #333;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
            }

            .topnav a {
                float: left;
                color: #f2f2f2;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                font-size: 17px;
            }

            .topnav a:hover {
                background-color: #ddd;
                color: black;
            }

            .topnav a.active {
                background-color: #04AA6D;
                color: white;
            }

            #sidebarMenu {
                height: 100%;
                position: fixed;
                left: 0;
                width: 250px;
                margin-top: 60px;
                transform: translateX(-250px);
                transition: transform 250ms ease-in-out;
                background: linear-gradient(180deg, #00FFAA 0%, #00AAFF 100%);
            }

            .sidebarMenuInner {
                margin: 0;
                padding: 0;
                border-top: 1px solid rgba(255, 255, 255, 0.10);
            }

            .sidebarMenuInner li {
                list-style: none;
                color: #fff;
                text-transform: uppercase;
                font-weight: bold;
                padding: 20px;
                cursor: pointer;
                border-bottom: 1px solid rgba(255, 255, 255, 0.10);
            }

            .sidebarMenuInner li a {
                color: #fff;
                text-transform: uppercase;
                font-weight: bold;
                cursor: pointer;
                text-decoration: none;
            }

            input[type="checkbox"]:checked ~ #sidebarMenu {
                transform: translateX(0);
            }

            input[type=checkbox] {
                transition: all 0.3s;
                box-sizing: border-box;
                display: none;
            }

            .popupDiv {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 100;
                opacity: 0;
                visibility: hidden;
                transition: all 0.25s;
            }

            input[id="popup"]:checked + .popupOpen + .popupDiv {
                opacity: 0.5;
                visibility: visible;
            }

            .popupDivDiv {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 350px;
                height: 250px;
                background: var(--uiLight);
                z-index: 2;
                border-radius: 20px;
                flex-direction: column;
                padding: 20px;
            }

            .darkModeSwitch {
                margin-top: 20px;
            }

            .darkModeButton {
                display: none;
            }

            .darkModeSlider {
                position: absolute;
                width: 100%;
                height: 20px;
                border-radius: 10px;
                transition: 0.3s;
            }

            .darkModeButton:checked ~ .darkModeSlider {
                background-color: var(--dark);
            }

            .darkModeButton:checked ~ .darkModeSlider::before {
                transform: translateX(19px);
                background-color: var(--light);
                box-shadow: none;
            }

            body {
                padding-top: 60px; /* Adjust for the fixed navbar */
            }
        </style>
    </head>
    <body id="darkModeElse">
        <div class="topnav">
            <a class="active" href="#home">Home</a>
            <a href="#news">News</a>
            <a href="#contact">Contact</a>
            <a href="#about">About</a>
            <input type="checkbox" id="popup">
            <label for="popup" class="popupOpen">Settings</label>
        </div>

        <div class="popupDiv">
            <div class="popupDivDiv">
                <label class="popupLabel">Settings</label>
                <label class="darkModeLabel">Dark Mode</label>
                <div class='darkModeSwitch'>
                    <label class="darkModeSwitchLabel">
                        <input id="darkModeSwitch" class="darkModeButton" type='checkbox' onclick="turnDarkMode();">
                        <span class='darkModeSlider'></span>
                    </label>
                </div>
                <label for="popup" class="popupClose">Close</label>
            </div>
        </div>

        <div id="sidebarMenu">
            <ul class="sidebarMenuInner">
                <li>Jelena Jovanovic <span>Web Developer</span></li>
                <li><a href="https://plancke.io/hypixel/player/stats/I_am_jake1104" target="_blank">Minecraft</a></li>
                <li><a href="https://web.roblox.com/users/1419405185/profile" target="_blank">Roblox</a></li>
                <li><a href="https://discord.gg/QSttQavQzV" target="_blank">Discord</a></li>
                <li><a href="https://www.youtube.com/channel/UCMmfv4GVlT7GfrEdg3GnYqQ" target="_blank">Youtube: 제이크-Jake</a></li>
                <li><a href="https://www.youtube.com/channel/UCZBC6nBxFfQWjQwf-Ig0MTg" target="_blank">Youtube: 제이크의 코딩 채널</a></li>
            </ul>
        </div>

        <input type="checkbox" class="openSidebarMenu" id="openSidebarMenu">
        <label for="openSidebarMenu" class="sidebarIconToggle">
            <div class="spinner diagonal part-1"></div>
            <div class="spinner horizontal"></div>
            <div class="spinner diagonal part-2"></div>
        </label>

        <div style="padding-left:16px;">
            <h2>사이트 소개</h2>
            <p>이곳은 여러분이 다양한 정보를 입력하고 공유할 수 있는 공간입니다. 많은 이용 부탁드립니다!</p>
        </div>

        <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
        <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
        
        <script>
            let isDarkMode = false;
            const darkModeContent = document.querySelectorAll('#darkModeContent');
            const darkModeElse = document.querySelectorAll('#darkModeElse');

            function turnDarkMode() {
                isDarkMode = !isDarkMode;
                document.body.style.background = isDarkMode ? "var(--uiDark)" : "var(--uiLight)";
                darkModeContent.forEach((content) => {
                    content.style.color = isDarkMode ? "var(--light)" : "var(--dark)";
                });
                darkModeElse.forEach((content) => {
                    content.style.background = isDarkMode ? "var(--dark)" : "var(--light)";
                });
            }
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
