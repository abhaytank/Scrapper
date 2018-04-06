from bs4 import BeautifulSoup

class SearchWeb():
    global db
    db = {}
    global maindomain
    maindomain = "http://www.tutorialspoint.com"
    global domain
    domain = { "java":"http://www.tutorialspoint.com/java/",
                "assembly_programming":"https://www.tutorialspoint.com/assembly_programming/index.htm",
                "cplusplus":"https://www.tutorialspoint.com/cplusplus/index.htm",
                "cpp_standard_library":"https://www.tutorialspoint.com/cpp_standard_library/index.htm",
                "cprogramming":"https://www.tutorialspoint.com/cprogramming/index.htm",
                "data_structures_algorithms":"https://www.tutorialspoint.com/data_structures_algorithms/index.htm",
                "learn_c_by_examples":"https://www.tutorialspoint.com/learn_c_by_examples/index.htm",
                "objective_c":"https://www.tutorialspoint.com/objective_c/index.htm",
                "jsp":"https://www.tutorialspoint.com/jsp/index.htm",
                "html":"https://www.tutorialspoint.com/html/index.htm",
                "bootstrap":"https://www.tutorialspoint.com/bootstrap/index.htm",
                "cpanel":"https://www.tutorialspoint.com/cpanel/index.htm",
                "css":"https://www.tutorialspoint.com/css/index.htm"}


    
    def __init__(self):
        global count
        count = 0
        global i
        i = 1
        global index
        index = {}
        global graph
        graph = {}
        for e in domain:
            print e
            global domainword
            domainword = e
            if i <= len(domain):
                count = count + 1
                print count
                self.finalranks( domain.get(domainword) , 50 , domainword , index , graph)
        print "Computing Ranks"
        global ranks
        ranks = self.computeRanks(graph)
        print "Ranks Computed"
        global corpus
        corpus = [index , ranks]
        return None

    def returncorp(self):
        return corpus
    
    def getPage(self, url):
        try:        
            import urllib
            pdf = url.find('pdf')
            if pdf != -1:
                return "" 
            print "Getting Page Source for", url
            return urllib.urlopen(url).read()
        except:
            print "Page Source Error for", url
            return ""


    def getAllLinks(self, url , page , domainword1):
        links = []
        soup = BeautifulSoup(page, 'html.parser')
        try:
            title1 = soup.title.string
            db[url] = title1
        except:
            ""
        for url in soup.find_all('a'):
            link = url.get('href')
            if link:
                if link.find(domainword1) > -1:
                    if (link.find('http')) == -1:
                        link = maindomain + link
                    links.append(link)       
        return links

    def union(self, tocrawlList, getAllLinksList):
        for e in getAllLinksList:
            if e not in tocrawlList:
                tocrawlList.append(e)


    def webCrawl(self, seed, max_pages , domainword2 ,count , index , graph):
        crawled = []
        tocrawl = [seed]
        for current_url in tocrawl:
            if current_url not in crawled and len(crawled) < max_pages:
                content = self.getPage(current_url)            
                outlinks = self.getAllLinks( current_url ,content , domainword2)            
                self.addPageToIndex(index, current_url, content)
                self.union(tocrawl, outlinks)
                graph[current_url] = outlinks
                crawled.append(current_url)
                print "Length of Tocrawl = ", len(tocrawl)
                print "Length of Crawled = ", len(crawled)

    def finalranks(self, seed, max_pages , domainword2 , index , graph):
        ranks = {}
        self.webCrawl(seed, max_pages , domainword2 ,count , index , graph)
        print "final rank count"
        print count

    def addPageToIndex(self, index, url, content):
        words = content.split()
        for word in words:
            word = word.lower()
            self.addToIndex(index, url, word)


    def addToIndex(self, index, url, keyword):
        if keyword in index:
            if url not in index[keyword]:
                index[keyword].append(url)
            return
        index[keyword] = [url]


    def lookup(self, index, keyword):
        if keyword in index:
            return index[keyword]
        return None


    def computeRanks(self, graph):
        d = 0.8
        ranks = {}
        numloops = 10
        npages = len(graph)
        for current_url in graph:
            ranks[current_url] = 1.0 / npages
        for i in range(0, numloops):
            newranks = {}
            for current_url in graph:
                newrank = (1 - d) / npages
                for node in graph:
                    if current_url in graph[node]:
                        newrank = newrank + d * (ranks[node] / len(graph[node]))
                newranks[current_url] = newrank
            ranks = newranks
        return ranks


    def orderedSearch(self, corpus, query):
        result = self.lookup(corpus[0], query)
        return self.quicksortRanks(result, corpus[1])

    def multiSearch(self, corpus, keyword):
        result_buffer = []
        common_results = []
        words = keyword.split()
        print words
        for e in words:
            temp_buffer = self.lookup(corpus[0], e)
            if temp_buffer:
                result_buffer.extend(temp_buffer)
        length = len(words)
        for e in result_buffer:
            if result_buffer.count(e) == length:
                if e not in common_results:
                    common_results.append(e)
                    try:
                        title = db.get(e)
                        for k in words:
                                if title.find(k):
                                    ranks[e] = ranks.get(e) + 1
                    except:
                        ""
        return self.quicksortRanks(common_results, corpus[1])
     

    def quicksortRanks(self, pages, ranks):
        if not pages or len(pages) <= 1:
            return pages
        else:
            pivot = ranks[pages[0]]
            lower = []
            higher = []
            for page in pages[1:]:
                if ranks[page] <= pivot:
                    lower.append(page)
                else:
                    higher.append(page)
        return self.quicksortRanks(higher, ranks) + [pages[0]] + self.quicksortRanks(lower, ranks)

    
    def get(self, query ,corpus ):
        print query
        return self.multiSearch(corpus, query)    



    

global obj
obj = SearchWeb()
