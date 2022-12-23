
# final.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP messenging program.


import tkinter as tk
from Profile import Post, Profile
from tkinter import BOTTOM, ttk, filedialog, font
from ds_messenger import DirectMessage, DirectMessenger
import time

updating = None
# dsu ip 168.235.86.101

class Pop():
    """
    A subclass of that will be responsible for the pop-up frame when 
    adding a new user or editing profile
    """
    def __init__(self, mas, option=None, info=None) -> None:
        self.option = option
        self.info = info
        self.pop = tk.Toplevel(mas)
        self.bigBold = font.Font(size=9, weight='bold')
        self.pop.geometry('240x120')

    def give_text(self):
        """
        Returns text inside user_entry widget then destorys pop-up frame
        """
        text = self.user_entry.get()
        self.pop.destroy()
        return text
    
    def _draw(self, file:bool):
        """
        Call only once, upon initialization to add widgets to pop-up frame of adding user
        """
        if not file:
            tk.Label(self.pop, text='Please create or open a profile first', font=self.bigBold).pack(pady=(20,5), padx=5)
            tk.Button(self.pop, text='Exit', command=self.pop.destroy, width=8).pack(pady=5)
        else:
            self.new_user = tk.Label(self.pop, text='Enter the user\'s username')
            self.new_user.pack(pady=(8,2), padx=5)
            self.user_entry = tk.Entry(self.pop, width=25)
            self.user_entry.pack(pady=5)
    
    def _draw2(self, file:bool):
        """
        Call only once, upon initialization to add widgets to pop-up frame of editing profile
        """
        if not file:
            tk.Label(self.pop, text='Please create or open a profile first', font=self.bigBold).pack(pady=(20,5), padx=5)
            tk.Button(self.pop, text='Exit', command=self.pop.destroy, width=8).pack(pady=5)
        else:
            tk.Label(self.pop, text='Enter a new '+ self.option).pack(pady=(8,0), padx=5)
            tk.Label(self.pop, text='Current: '+ self.info).pack()
            self.user_entry = tk.Entry(self.pop, width=25)
            self.user_entry.pack(pady=5)

class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._msgs = [DirectMessage]
        self._posts = [Post]
        self._users = []
        self.sender = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    def node_select(self, event):
        """
        Update the messages_box with the full messaging history when the corresponding node in the users_tree
        is selected.
        """
        index = int(self.users_tree.selection()[0])
        #print(index, self._users)
        self.set_text_box(self._users[index])
        self.sender = self._users[index]
        self.user_label.configure(text=self.sender)
    
    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """
        return self.entry_editor.get('1.0', 'end').rstrip()

    
    def set_text_box(self, user):
        """
        Sets the messages to be displayed in the messages_box widget.
        """
        #print(2, self._users)
        all_msg = []
        l, s = [], []
        """
        All posts and messages are ordered chronoloigcally, oldest to latest
        """
        if user in self._posts:
            l = list(self._posts[user])
        if user in self._msgs:
            s = list(self._msgs[user])
        while s and l:
            a, b = s[0], l[0]
            if float(a[1])<float(b[1]):
                all_msg.append(a)
                s.pop(0)
            else:
                all_msg.append(b)
                l.pop(0)
        if s:
            all_msg.extend(s)
        elif l:
            all_msg.extend(l)
        
        """
        Configures two tags that specificy which entries were received by the user or which were sent from the user.
        Inserts messages into messages_box with their resepctive tags.
        """
        self.messages_box['state'] = 'normal'
        self.messages_box.delete(0.0, 'end')
        self.messages_box.tag_configure('my', justify='right', background='#2E86C1')
        self.messages_box.tag_configure('your', justify='left')
        for id in all_msg:
            if id[2] == 0:
                self.messages_box.insert('end', id[0]+'\n', 'my')
            elif id[2] == 1:
                self.messages_box.insert('end', id[0]+'\n', 'your')
        self.messages_box['state'] = 'disabled'
            
    def set_posts(self, msgs:list, posts:list):
        """
        Populates the self._posts attribute with posts from the active DSU file.
        Populates the self._msgs attribute with messages from the active DSU file.
        Populates the self._users attribute with usernames of all interactions from DSU file.
        """
        #print(3, self._users)
        temp = {}
        for i in msgs:
            if i['recipient'] not in temp:
                temp[i['recipient']] = [(i['entry'], i['timestamp'], 1)]
            else:
                temp[i['recipient']].append((i['entry'], i['timestamp'], 1))
        self._msgs = temp
        temp = {}
        for i in posts:
            if i['sender'] not in temp:
                temp[i['sender']] = [(i['entry'], i['timestamp'], 0)]
            else:
                temp[i['sender']].append((i['entry'], i['timestamp'], 0))
        self._posts = temp
        self._users.extend(list(self._msgs.keys()))
        self._users.extend(list(self._posts.keys()))
        self._users = list(dict.fromkeys(self._users))
        for id in range(len(self._users)):
            self._insert_users_tree(id, self._users[id])

    
    def insert_user(self, user):
        """
        Inserts a new user to the users_tree widget.
        """
        if user in self._users:
            self.sender = user
            index = self._users.index(user)
            self.set_text_box(self._users[index])
        else:
            self.sender = user
            self._users.append(user)
            id = len(self._users) - 1 #adjust id for 0-base of treeview widget
            self._insert_users_tree(id, user)
            #print(1, self._users)
        self.user_label.configure(text=self.sender)

    
    def reset_ui(self):
        """
        Clears messages_box and users_tree widgets to their default state. 
        Useful for clearing the UI is neccessary such as when a new DSU file is loaded or updating messages.
        """
        self.messages_box['state'] = 'normal'
        self.messages_box.delete(0.0, 'end')
        self.messages_box['state'] = 'disabled'

        #self.entry_editor.delete(0.0, 'end')
        self.entry_editor.configure(state=tk.NORMAL)
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

    
    def _insert_users_tree(self, id, user):
        """
        Inserts a user entry into the users_tree widget.
        """
        self.users_tree.insert('', id, id, text=user)
    
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.users_tree = ttk.Treeview(posts_frame)
        self.users_tree.bind("<<TreeviewSelect>>", self.node_select) # 
        self.users_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=2)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame)
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.user_label = tk.Label(editor_frame, text='', font=('Segoe UI', 10, 'bold'), fg='#4b4b4b')
        self.user_label.pack(fill=tk.Y, side=tk.TOP, anchor=tk.W, padx=20)

        self.messages_box = tk.Text(editor_frame, wrap='word',height=20)
        self.messages_box.configure(font=('Segoe UI', 10))
        self.messages_box.pack(fill=tk.BOTH, side=tk.TOP, expand=True, pady=1)
        self.messages_box['state'] = 'disabled'

        self.entry_editor = tk.Text(editor_frame, height=4, wrap='word')
        self.entry_editor.configure(font=('Segoe UI', 10))
        self.entry_editor.pack(fill=tk.BOTH, side=tk.TOP, pady=(2,2))
        
        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, send_callback=None, add_callback=None, update_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_callback = add_callback
        self._update_callback = update_callback
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    def send_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._send_callback is not None:
            self._send_callback()

    def update_click(self):
        """
        Calls callback function in update_callback class attribute, if available,
        when the update_button has been clicked
        """
        if self._update_callback is not None:
            self._update_callback()

    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)
    
    def add_click(self):
        """
        Calls callback function specific in the add_callback class attribute, if
        available, when the add_button has been clicked.
        """
        if self._add_callback is not None:
            self._add_callback()

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        fancyFont = font.Font(family='Segoe UI', size=9)
        save_button = tk.Button(master=self, text="Send", width=20, bg='#21618C', font=fancyFont, fg='white')
        save_button.configure(command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        updt_button = tk.Button(master=self, text="Update", width=15, font=fancyFont)
        updt_button.configure(command=self.update_click)
        updt_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        add_button = tk.Button(master=self, text='Add User', width=10, bg='#21618C', fg='white', font=fancyFont)
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=12, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=10)

        self.footer_user = tk.Label(master=self, text='')
        self.footer_user.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the Profile class and DirectMessenging class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = Profile()
        self._messenger_profile = None
        self._profile_filename = None
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        
        self._profile_filename = filename.name
        self.body._users = []
        self._current_profile = Profile()
        self._current_profile.dsuserver = '168.235.86.101'
        self._current_profile.save_profile(self._profile_filename)
        self._messenger_profile = None
        self.body._posts = [Post]
        self.body._msgs = [DirectMessage]
        self.body._users = []
        self.body.reset_ui()
        self.body.user_label.configure(text='')
    
    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        self._profile_filename = filename.name
        self._current_profile = Profile()
        self._current_profile.load_profile(self._profile_filename)
        usr = self._current_profile.username
        pwd = self._current_profile.password
        srv = self._current_profile.dsuserver
        try:
            self._messenger_profile = DirectMessenger(srv, usr, pwd)
            temp = self._messenger_profile.retrieve_all()
        except:
            self.footer.set_status('Unable to connect to DS server')
            temp = self._current_profile._messages
        self._current_profile.store_messages(temp)
        self.body._posts = [Post]
        self.body._msgs = [DirectMessage]
        self.body._users = []
        #print(self._current_profile.get_posts())
        self.body.reset_ui()
        self.body.user_label.configure(text='')
        self.body.set_posts(self._current_profile.get_messages(), self._current_profile.get_posts())

    
    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    def send_msg(self):
        """
        Sends the text currently in the entry_editor widget to the user selected
        or added from the users_tree widget.
        """
        """
        Does not send text if user has yet to complete a profile
        """
        if self._profile_filename == None:
            self.footer.set_status('Missing profile')
        elif self._current_profile.username == None:
            self.footer.set_status('Missing username')
        elif self._current_profile.password == None:
            self.footer.set_status('Missing password')
        elif self._current_profile.dsuserver == None:
            self.footer.set_status('Missing server')
        elif self.body.sender == None:
            self.footer.set_status('No sender')
        else:
            if self.body.get_text_entry() and self._messenger_profile.send(self.body.get_text_entry(), self.body.sender):
                post = Post(self.body.sender, self.body.get_text_entry())
                self._current_profile.add_post(post)
                self._current_profile.save_profile(self._profile_filename)
                self.update()
                self.body.entry_editor.delete(0.0, 'end')
            self.restart_update()

    def edit_profile(self, option):
        """
        sets info variable to the param option which is used to inform the user what variable they will edit, sets as "n/a" if empty variable
        """
        if option == 'username':
            info = self._current_profile.username if self._current_profile.username else 'n/a'
        elif option == 'password':
            info = self._current_profile.password if self._current_profile.password else 'n/a'
        elif option == 'server':
            info = self._current_profile.dsuserver if self._current_profile.dsuserver else 'n/a'

        """
        creates pop-up window that closes and returns the text in the entry box 
        """
        self.update()
        self.new = Pop(self.root, option, info)
        file_path = False if self._profile_filename == None else True
        self.new._draw2(file_path)
        if file_path:
            tk.Button(self.new.pop, text='Submit', command=lambda: self.submit(option)).pack(pady=(0,10))

    
    def submit(self, option=None):
        """
        Button command for the pop-up window. Sets entry as the new variable and saves profile
        """
        #print('submitting...')
        entry = self.new.give_text()
        if option == 'username':
            self._current_profile.username = entry
            self.footer.set_status('Username changed')
        elif option == 'password':
            self._current_profile.password = entry
            self.footer.set_status('Password changed')
        elif option == 'server':
            self._current_profile.dsuserver = entry
            self.footer.set_status('Server changed')
        usr = self._current_profile.username
        pwd = self._current_profile.password
        srv = self._current_profile.dsuserver
        if usr and pwd:
            print(usr, pwd, srv)
            try:
                self._messenger_profile = DirectMessenger(srv, usr, pwd)
            except:
                self.footer.set_status('Unable to connect to DS server')
        self._current_profile.save_profile(self._profile_filename)
        self.restart_update()

    def add_user(self):
        """
        Opens pop-up window that will add a new user to message
        """ 
        self.update()
        self.new = Pop(self.root)
        file_path = False if self._profile_filename == None else True
        self.new._draw(file_path)
        if file_path:
            tk.Button(self.new.pop, text='Submit', command=self.add).pack(pady=(0,10))
    
    def add(self):
        """
        Adds new user to treeview
        """
        entry = self.new.give_text()
        self.body.insert_user(entry)
        self.body.set_text_box(self.body.sender)
    
    def update_msg(self):
        """
        Updates messages_box with any new msgs and adds another update event after 2 sec
        """
        #print('updating...')
        global updating
        if self._profile_filename != None:
            try:
                all = self._current_profile.get_messages()
                temp = self._messenger_profile.retrieve_new()
                all.extend(temp)     
                self._current_profile.store_messages(all)
                self._current_profile.save_profile(self._profile_filename)
                self.body.reset_ui()
                self.body.set_posts(self._current_profile.get_messages(), self._current_profile.get_posts())
                self.body.set_text_box(self.body.sender)    
                updating = self.body.after(3000, self.update_msg)
            except:
                if self._current_profile.username and self._current_profile.password:
                    try:
                        usr = self._current_profile.username
                        pwd = self._current_profile.password
                        srv = self._current_profile.dsuserver
                        self._messenger_profile = DirectMessenger(srv, usr, pwd)
                        self.footer.set_status('Invalid password or username taken')
                    except:
                        self.footer.set_status('Unable to connect to DS server')
                else:
                    self.footer.set_status('Incomplete profile')
        else:
            updating = self.body.after(3000, self.update_msg)
    
    def restart_update(self):
        """
        Clears event loop with any updating event and immediately updates msg box 
        """
        global updating
        if updating:
            self.body.after_cancel(updating)
        if self._messenger_profile:
            all = self._messenger_profile.retrieve_all()     
            self._current_profile.store_messages(all)
        updating = self.update_msg()
    
    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='Edit')
        menu_file.add_command(label='Username', command=lambda: self.edit_profile('username'))
        menu_file.add_command(label='Password', command=lambda: self.edit_profile('password'))
        menu_file.add_command(label='Server', command=lambda: self.edit_profile('server'))

        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, send_callback=self.send_msg, add_callback=self.add_user, update_callback=self.restart_update)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Messenger Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x540")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.after(3000, app.restart_update)
    main.mainloop()