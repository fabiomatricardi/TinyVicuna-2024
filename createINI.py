import configparser


def create_config():
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config['Model'] = {'name': 'tiny-vicuna-1b', 'file': 'tiny-vicuna-1b.q6_k.gguf', 
                       'NCTX' : 2048, 'STOPS': ["<s>"]}
    config['UI'] = {'myheader': 'Powerwed by Tiny Vicuna 1B, the best 1B Instruction model before Qwen',
                          'cursor': "🟡", 'av_us' : '🧑‍💻', 'av_ass' : '🦙'}  
                          #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". 😁🤖🧔‍♂️🧞‍♂️🔮🩻🪆🌀🟡🟨💬♦️ Shortcodes are not supported.


    # Write the configuration to a file
    with open('tiny-vicuna-1b.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    create_config()