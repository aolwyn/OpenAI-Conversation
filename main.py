import os
import random
import openai
import time
import names
import re 
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv

# Initialize the Tkinter window 
root = tk.Tk()
root.geometry('600x400')
root.attributes('-topmost',1) 
root.resizable(False, False) 
mainframe = tk.Frame(root, background='white')
mainframe.pack(fill='both', expand=True)

load_dotenv()

API_KEY = None
root = tk.Tk()
root.geometry("600x600")
mainframe = ttk.Frame(root)
mainframe.pack(fill='both', expand=True)

def openAIKey:
  api_key = os.getenv('OPENAI_API_KEY')

  if api_key:
    return api_key
  else:
    print("API Key not found in the .env file.")
  


def main():
    openai.api_key = openAIKey()  # Initializes AI

    named_mode = prompt_yes_no('Would you like to enter celebrity mode?', 17)

    ai_1_properties = get_ai_properties(named_mode, 1)
    ai_2_properties = get_ai_properties(named_mode, 2)

    random_changes = prompt_yes_no('Would you like random changes to take place in the conversation?', 14)

    limit = get_text('Set the amount of messages you\'d like the bots to have', 14)
    while not limit.isdigit():
        limit = get_text('Set the amount of messages you\'d like the bots to have', 14)

    limit = str(int(limit) // 2)  # 2 messages per loop

    prompt1 = get_text(f'Enter an initial prompt to get the conversation going ({ai_2_properties.name} -> {ai_1_properties.name})', 13)

    log_file = open(f'./logs/{ai_1_properties.name.replace(" ","_")}_and_{ai_2_properties.name.replace(" ","_")}_{time.time()}_conversation-log.txt', 'x')
    
    print_simulation_info(named_mode, ai_1_properties, ai_2_properties, prompt1, limit, log_file) 

    if named_mode == 'y':
        ai_1_messages = [{"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for. Do not include pleasantries in your responses."}, 
                         {"role": "system", "content": ai_2_properties.name + " and you are together somewhere, and they say something to you: "},
                         {"role": "user", "content": str(prompt1)}, 
                         {"role": "assistant", "content": str(get_message_from_ai1([{"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}]))}]

        ai_2_messages = [{"role": "system", "content": "Act like you are " + ai_2_properties.name + " and never leave that role, even if you are asked for. Do not include pleasantries in your responses."},
                         {"role": "system", "content": "You and " + ai_1_properties.name + " are together somewhere, and you engage in conversation by saying: "},
                         {"role": "assistant", "content": str(prompt1)}, 
                         {"role": "user", "content": str(get_message_from_ai1([{"role": "system", "content": "Act like you are " + ai_2_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}]))}]
    else:
        ai_1_messages = [{"role": "system", "content": "You are a human living named " + ai_1_properties.name + ", living on Earth and you will have to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_1_properties.age) +  " years old and you are a " + str(ai_1_properties.gender) +". Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person. Try to change the topic sometimes, conversating about the same topic for a long time can be boring! Do not include pleasantries in your responses."},
                         {"role": "system", "content": ai_2_properties.name + ", a " + ai_2_properties.age + " year old " + ai_2_properties.gender + ", and you are together somewhere, and they say something to you: "},
                         {"role": "user", "content": str(prompt1)}, 
                         {"role": "assistant", "content": str(get_message_from_ai1([{"role": "system", "content": "You are a human living named " + ai_1_properties.name + ". You are a " + str(ai_1_properties.age) + " year old " + ai_1_properties.gender + ", and you need to consider your age and gender and a corresponding education level and hypothetical life experiences for the way you talk and what you are interested or will talk about. Never leave this role, EVER. Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}]))}]

        ai_2_messages = [{"role": "system", "content": "You are a human living named " + ai_2_properties.name + ". You are a " + str(ai_2_properties.age) + " year old " + ai_2_properties.gender + ", and you need to consider your age and gender and a corresponding education level and hypothetical life experiences for the way you talk and what you are interested or will talk about. Never leave this role, EVER. Do not include pleasantries in your responses."},
                         {"role": "system", "content": "You and " + ai_1_properties.name + ", a " + ai_1_properties.age + " year old " + ai_1_properties.gender + ", are together somewhere, and you engage in conversation by saying: "},
                         {"role": "assistant", "content": str(prompt1)}, 
                         {"role": "user", "content": str(get_message_from_ai1([{"role": "system", "content": "You are a human living named " + ai_2_properties.name + ". You are a " + str(ai_2_properties.age) + " year old " + ai_2_properties.gender + ", and you need to consider your age and gender and a corresponding education level and hypothetical life experiences for the way you talk and what you are interested or will talk about. Never leave this role, EVER. Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}]))}]

    start_time = time.time() 
    add_gui_log(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:0): {ai_1_messages[3]['content']}\n", log_file) 
    random_seed = random.randint(1, 2) 

    happened_last = 0 
    for i in range(int(limit)): 
        root.after(2000) 
        ai_2_message = get_message_from_ai2(ai_2_messages) 
        ai_2_messages.append({'role': 'assistant', 'content': ai_2_message}) 
        ai_1messages.append({'role': 'user', 'content': ai_2_message}) 
        add_gui_log(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) 
        add_gui_log('\n---------------------------------------------------------------------------------------\n', log_file) 
        root.after(2000) 

        random_conversation_switcher = random.randint(1, 2) 

        if random_changes == 'n':
            random_conversation_switcher = 0 

        if random_conversation_switcher == random_seed and happened_last + 3 <= i:
            add_gui_log(f'Suddenly... a random force makes {ai_1_properties.name} want to talk about something else...', log_file)
            if random.randint(1, 2) == 1:
                ai_1_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
            else:
                ai_1_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
            happened_last = i 
            add_gui_log('\n---------------------------------------------------------------------------------------\n', log_file)

        ai_1_message = get_message_from_ai1(ai_1_messages)
        ai_2_messages.append({'role': 'user', 'content': ai_1_message}) 
        ai_1_messages.append({'role': 'assistant', 'content': ai_1_message}) 
        add_gui_log(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:{i+1}): {ai_1_message}\n", log_file) 

        if random_conversation_switcher == random_seed and happened_last + 3 <= i:
            add_gui_log('\n---------------------------------------------------------------------------------------\n', log_file)
            add_gui_log(f'Suddenly... a random force makes {ai_2_properties.name} want to talk about something else...', log_file)
            if random.randint(1, 2) == 1:
                ai_2_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
            else:
                ai_2_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
            happened_last = i 
            add_gui_log('\n---------------------------------------------------------------------------------------\n', log_file)

    ai_2_message = get_message_from_ai2(ai_2_messages)
    add_gui_log(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) 
    add_gui_log('\n====================================================\n', log_file) 
    add_gui_log(f'{(int(limit))*2 + 2} messages sent in {int(time.time() - start_time)} seconds.', log_file) 
    root.title(f'{ai_1_properties.name} and {ai_2_properties.name} had a conversation ') 

def prompt_yes_no(prompt, font_size):
    text = ttk.Label(mainframe, text=prompt, wraplength=550, background='white', font=('Brass Mono', font_size), justify='center')
    text.place(relx=.5, rely=.4, anchor="c")
    answer = tk.StringVar(value='y')
    answer_button_clicked = tk.StringVar() 

    radio_button_yes = ttk.Radiobutton(mainframe, text='Yes', variable=answer, value='y')
    radio_button_no = ttk.Radiobutton(mainframe, text='No', variable=answer, value='n')
    radio_button_yes.place(relx=.4, rely=.55, anchor="c")
    radio_button_no.place(relx=.6, rely=.55, anchor="c")

    submit_yes_no = ttk.Button(mainframe, text='Submit Choice', command=lambda: answer_button_clicked.set('clicked'))
    submit_yes_no.place(relx=.5, rely=.7, anchor="c")

    submit_yes_no.wait_variable(answer_button_clicked) 
    clear_mainframe()

    return answer.get() 

def get_text(prompt, font_size):
    text = ttk.Label(mainframe, text=prompt, wraplength=550, background='white', font=('Brass Mono', font_size), justify='center')
    text.place(relx=.5, rely=.4, anchor="c")
    answer_button_clicked = tk.StringVar() 

    text_input = ttk.Entry(mainframe, width=70) 
    text_input.place(relx=.5, rely=.6, anchor="c")

    submit_input = ttk.Button(mainframe, text='Submit Choice', command=lambda: answer_button_clicked.set('clicked'))
    submit_input.place(relx=.5, rely=.7, anchor="c")

    submit_input.wait_variable(answer_button_clicked) 
    result = text_input.get() 
    clear_mainframe()
    return result

def add_gui_log(text, log_file):
    text_gui = ttk.Label(secondframe, text=text, background='white', font=('Brass Mono', 12), justify='left', padding=4, width=600, wraplength=560)
    text_gui.pack()
    log_file.write(text)

def get_message_from_ai1(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content.strip()

def get_message_from_ai2(messages):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.6
    )

    return response.choices[0].message.content.strip()

def text_popup(main_text, sub_text, popup_time):
    starting_var = tk.StringVar()
    starting_text = ttk.Label(mainframe, wraplength=550, text=main_text, background='white', font=('Brass Mono', 14), justify='center')
    starting_subtext = ttk.Label(mainframe, wraplength=550, text=sub_text, background='white', font=('Brass Mono', 10), justify='center')
    starting_text.place(relx=0.5, rely=0.4, anchor='c')
    starting_subtext.place(relx=0.5, rely=0.6, anchor='c')

    root.after(popup_time, func=lambda: starting_var.set('starting'))
    starting_text.wait_variable(starting_var)
    clear_mainframe()

def get_ai_properties(named_mode, number):
    class AI_Information():
        def __init__(self, named_mode):
            self.age = str(random.randint(18, 82)) 
            self.gender = self.get_gender()
            self.name = self.get_name(named_mode)
            self.number = number 

        def get_gender(self): 
            rand_number = random.randint(1, 2)
            if rand_number == 1:
                return 'male'
            else:
                return 'female'

        def get_name(self, named_mode): 
            if named_mode == 'y':
                return get_text(f'Enter the name of the person you would like AI agent #{number} to become: ', 13) 
            return names.get_first_name(gender=self.gender)

    new_ai = AI_Information(named_mode)
    return new_ai 

def print_simulation_info(named_mode, ai_1, ai_2, prompt1, limit, log_file):
    root.after(1000)
    add_gui_log('Initializing AI...', log_file)
    add_gui_log('\n====================================================\n', log_file)
    add_gui_log(f'Initial prompt ({ai_2.name} -> {ai_1.name}): ' + prompt1 + '\n', log_file)
    if (named_mode != 'y'):
        add_gui_log(f'AI 1 Details:\n\tAge: {ai_1.age}\n\tGender: {ai_1.gender}\n\tName: {ai_1.name}', log_file)
        add_gui_log(f'\nAI 2 Details:\n\tAge: {ai_2.age}\n\tGender: {ai_2.gender}\n\tName: {ai_2.name}', log_file)
        add_gui_log(f'\nCelebrity Mode: Disabled', log_file)
    else:
        add_gui_log(f'AI 1 Details:\n\tName: {ai_1.name}', log_file)
        add_gui_log(f'AI 2 Details:\n\tName: {ai_2.name}', log_file)
        add_gui_log(f'\nCelebrity Mode: Enabled', log_file)

    add_gui_log('\nMessage Limit: ' + limit * 2, log_file)
    add_gui_log('\n====================================================\n', log_file)
    add_gui_log('Initializing conversation...', log_file)
    add_gui_log('\n====================================================\n', log_file)

if __name__ == '__main__':
    
    text_popup('Using OpenAI API', 'Note: Requires OpenAI credits.', 2000)
    API_KEY = openAIKey()
    if API_KEY:
        main()
    else:
        text_popup('No API Key was found in your environment variables', 'Please try again or input the key instead', 4000)
        exit()
    root.mainloop()

