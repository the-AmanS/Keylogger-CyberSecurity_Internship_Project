import os
from datetime import datetime
from nicegui import ui

LOG_FILE = "keylogs.txt"

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'a').close()

def handle_key(e):
    if not consent.value:
        return

    key_name = e.args['key']
    
    mods = []
    if e.args['ctrlKey']: mods.append('CTRL')
    if e.args['shiftKey']: mods.append('SHIFT')
    if e.args['altKey']: mods.append('ALT')
    
    display_key = f"{'+'.join(mods)}+{key_name}" if mods else key_name
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"{timestamp} | {display_key}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    log_display.value = log_entry + log_display.value

ui.query('body').style('background-color: #f0f2f5')

with ui.card().classes('fixed-center w-[450px] shadow-lg p-6'):
    ui.label('🔐 Real-Time Audit Tool').classes('text-h5 text-primary font-bold')
    ui.label('Internship Project - Phase 3').classes('text-subtitle2 text-grey-7 mb-4')
    
    consent = ui.checkbox('Enable Keystroke Monitoring')
    
    with ui.column().bind_visibility_from(consent, 'value').classes('w-full'):
        ui.label('Type inside this box:').classes('text-grey-9 mt-2')

        target_input = ui.input(placeholder='Capture active...') \
            .classes('w-full mb-4').props('outlined') \
            .on('keydown', handle_key, args=['key', 'ctrlKey', 'shiftKey', 'altKey'])
        
        ui.label('Live Exfiltration Feed:').classes('text-xs font-bold text-red-500 mt-2')
        log_display = ui.textarea().props('readonly filled') \
            .classes('w-full h-48 bg-grey-2 font-mono text-xs')

port = int(os.environ.get('PORT', 8080))
ui.run(title="Live Audit Demo", port=port, reload=False)