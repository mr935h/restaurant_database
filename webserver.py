from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import database_query

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                s = database_query.all_restaurants()
                for x in s:
                    a = x[1]
                    output += "<h2>"
                    output += str(a)
                    output += "</h2>"
                    output += "<a href='/restaurant/id/edit' name = " + str(a) + ">edit</a>"
                    output += "  "
                    output += "<a href='/restaurant/delete?var=" + str(a) + "'>delete</a>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Enter a new restaurant below</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant'><h2>What restaurant would you link to add?</h2>
                <input name="new_restaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/id/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant name</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant'>
                old name <input name="old_name" type="text">
                 new name <input name="new_name" type="text">
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                $var = $_GET['var']
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete this restaurant?</h1>"
                output += "<h2>" + $var + "</h2>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant'>
                old name <input name="old_name" type="text">
                 new name <input name="new_name" type="text">
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                oldname = fields.get('old_name')
                newname = fields.get('new_name')
                newrestaurant = fields.get('new_restaurant')

            if messagecontent is not None:
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output

            elif newrestaurant is not None:
                database_query.new_restaurant(newrestaurant)
                output = ""
                output += "<html><body>"
                s = database_query.all_restaurants()
                for x in s:
                    a = x[1]
                    output += "<h2>" + a + "</h2>"
                    output += "<a href='/restaurant/id/edit' name = " + str(a) + ">edit</a>"
                    output += "  "
                    output += "<a href="">delete</a>"
                self.wfile.write(output)
                print output

            elif oldname is not None:
                database_query.edit_restaurant(oldname, newname)
                output = ""
                output += "<html><body>"
                s = database_query.all_restaurants()
                for x in s:
                    a = x[1]
                    output += "<h2>" + a + "</h2>"
                    output += "<a href='/restaurant/id/edit' name = " + str(a) + ">edit</a>"
                    output += "  "
                    output += "<a href="">delete</a>"
                self.wfile.write(output)
                print output

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()