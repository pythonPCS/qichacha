import time
import random
from pyppeteer.launcher import launch
import asyncio
from alifunc import mouse_slide, input_time_random
from exe_js import js1, js3, js4, js5
import tkinter


async def main():
    print('开始')
    launch_kwargs = {
        # 控制是否为无头模式
        "headless": False,
        # chrome启动命令行参数
        "args": [
            # 浏览器代理 配合某些中间人代理使用
            # "--proxy-server=http://127.0.0.1:8008",
            # 最大化窗口
            "--start-maximized",
            # 取消沙盒模式 沙盒模式下权限太小
            "--no-sandbox",
            # 不显示信息栏  比如 chrome正在受到自动测试软件的控制 ...
            "--disable-infobars",
            # log等级设置 在某些不是那么完整的系统里 如果使用默认的日志等级 可能会出现一大堆的warning信息
            "--log-level=3",
            # 设置UA
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        ],
        # 用户数据保存目录 这个最好也自己指定一个目录
        # 如果不指定的话，chrome会自动新建一个临时目录使用，在浏览器退出的时候会自动删除临时目录
        # 在删除的时候可能会删除失败（不知道为什么会出现权限问题，我用的windows） 导致浏览器退出失败
        # 然后chrome进程就会一直没有退出 CPU就会狂飙到99%
        "userDataDir": "",
    }
    # browser = await launch({'headless': False, }) # headless为True，不弹出浏览器，为False弹出浏览器
    browser = await launch(launch_kwargs) # headless为True，不弹出浏览器，为False弹出浏览器
    page = await browser.newPage()
    # 浏览器默认开启大小为：800 * 600 一般是不够的
    """使用tkinter获取屏幕大小，并设置为最大"""
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    await page.setViewport({
        "width": width,
        "height": height
    })
    await page.goto('https://www.qichacha.com/user_login?back=%2F')
    # 通过加载js，防止pyppeteer被识别
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)
    # 输入Gmail
    await page.click("#normalLogin")
    time.sleep(2)
    await page.type('#nameNormal', '17601007385')
    await page.type('#pwdNormal', '092744gd')
    time.sleep(5)
    # 点击下一步
    print("开始滑动！")
    await page.hover('#nc_2_n1z')  # 不同场景的验证码模块能名字不同。
    await page.mouse.down()
    await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
    await page.mouse.up()
    time.sleep(5)
    await page.click('button') # 点击登录
    # flag = await mouse_slide
    await get_cookie(page)     # 获取cookie
    time.sleep(1000)


# 获取登录后cookie
async def get_cookie(page):
    res = await page.content() # 获取页面内容
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    print(cookies)
    return cookies

# 启动
loop = asyncio.get_event_loop()
loop.run_until_complete(main())





