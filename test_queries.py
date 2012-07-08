from pyes import *
class Foo():
    conn = ES('127.0.0.1:9200')
    conn.default_indices=["logstash-2012.07.04"]
    conn.refresh()
    print "i'm in"
    def main(self):
        q = TermQuery("agent", "\"SAMSUNG-SGH-E250i/E250iJAKA1 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0\"")
        #q = TermQuery("calling_id" ,"27820649562")
        results = self.conn.search(query = q)
        print "i'm okay"
        for r in results:
            print r
            print "kkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
            print
f = Foo()
f.main()

