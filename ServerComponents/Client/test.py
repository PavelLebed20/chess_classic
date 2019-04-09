
import ServerComponents.Client.client as cli

cl = cli.Client('http://localhost:8000')

cl.send_message('login', 'login=admin1&password=admin1')
