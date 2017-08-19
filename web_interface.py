import ConfigParser
import logging
import subprocess
import sys

from flask import Flask, render_template, request, redirect, url_for

from controller_config import Config
from switch_nexa import NexaSwitcher

app = Flask(__name__)


def read_logs(file_name='/run/nexa_controller.log'):
    try:
        with open(file_name, 'r') as f:
            return f.readlines()[-100:]
    except Exception as e:
        return "Can't read log file {}: {}".format(file_name, repr(e))


@app.route("/")
def ini_editor():
    config = Config()

    return render_template('ini_editor.html', message=request.args.get('message', ''), config=config, logs=read_logs())


@app.route("/reboot")
def reboot():
    subprocess.call("reboot", shell=True)
    return render_template('reboot_in_progress.html')


@app.route("/open")
def open_window():
    return switch_window_status(True)


@app.route("/close")
def close_window():
    return switch_window_status(False)


@app.route("/save_settings", methods=['POST'])
def save_settings():
    try:
        remount_partition('rw', '/')

        config = ConfigParser.ConfigParser()

        # do not change letter case
        config.optionxform = str

        config_file_name = 'controller_config.ini'
        read_files = config.read(config_file_name)
        if len(read_files) != 1:
            raise RuntimeError("Can't read {}".format(config_file_name))

        change_config_parameter(config, 'HARDWARE', 'RASPBERRY_PI_DATA_PIN')
        change_config_parameter_as_list(config, 'HARDWARE', 'TRANSMITTER_CODES')
        change_config_parameter(config, 'TIME', 'EARLIEST_ENABLE_HOUR')
        change_config_parameter(config, 'TIME', 'EARLIEST_ENABLE_MINUTE')
        change_config_parameter(config, 'TIME', 'LATEST_DISABLE_HOUR')
        change_config_parameter(config, 'TIME', 'LATEST_DISABLE_MINUTE')
        change_config_parameter(config, 'ROUTER', 'ROUTER_HOST')
        change_config_parameter(config, 'ROUTER', 'ROUTER_USERNAME')
        change_config_parameter(config, 'ROUTER', 'ROUTER_PASSWORD')
        change_config_parameter_as_list(config, 'ROUTER', 'MONITORED_MAC_ADRESSES')
        change_config_parameter(config, 'KODI', 'KODI_ADDR')
        change_config_parameter(config, 'DATADOG', 'DATADOG_API_KEY')
        change_config_parameter(config, 'DATADOG', 'DATATOG_METRIC_NAME')
        change_config_parameter(config, 'DATADOG', 'DATADOG_HOST_NAME')
        change_config_parameter(config, 'DATADOG', 'DATADOG_ON_VALUE')
        change_config_parameter(config, 'DATADOG', 'DATADOG_OFF_VALUE')

        with open(config_file_name, 'w') as f:
            config.write(f)

        message = 'Saved successfully. <a href="{}">Reboot the device</a> to apply the changes.'.format(
            url_for('reboot'))
    except Exception as e:
        message = 'Error: ' + str(e)
    finally:
        remount_partition('ro', '/')

    return redirect(url_for('ini_editor', message=message))


def change_config_parameter(config, section, name):
    existing_value = config.get(section, name, '')
    config.set(section, name, request.values.get(name, default=existing_value))


def change_config_parameter_as_list(config, section, name):
    new_value = request.values.get(name, '')

    if new_value != '':
        new_value = new_value.replace('\r', '')
        new_value = new_value.replace('\n', ',')

    config.set(section, name, new_value)


def remount_partition(mode, partition):
    try:
        subprocess.call("mount -o remount,{} {}".format(mode, partition), shell=True)
    except Exception:
        logging.exception("Can't remount partition {} {}".format(mode, partition))


def switch_window_status(is_open):
    config = Config()
    switcher = NexaSwitcher(config.RASPBERRY_PI_DATA_PIN, config.TRANSMITTER_CODES[0])
    switcher.switch(is_open)
    return "OK"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s %(message)s')
    app.run(host='0.0.0.0', port=8080)
