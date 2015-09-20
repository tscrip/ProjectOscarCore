from app import app as app
from app import core as Core

#Creating Core Object
CoreObj = Core.Core()

#Starting web server
app.run(debug=CoreObj.WebServerDebug,port=CoreObj.WebServerPort,threaded=True,host='0.0.0.0')
