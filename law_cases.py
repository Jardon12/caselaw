import requests
# this is a library that we use to pass http requests

# there are multiple pages potentially, because a search only includes 100 cases per page. So we open all the links and save each page.
def get_pages(url):
    page_list = []
    while True:
        # this is the only place in which we do a request and get the page from the online website case.law
        result = requests.get(url).json()

        # result is what the previous request returns. It is what accessing the URL will show on the page. This entire result we store in the list below:
        page_list.append(result)

        # then we get the URL for the next page that we want to load
        url = result['next']

        # if there is no URL is means that we have processed all the pages
        if not url:
            break
    # page_list is the list that contains all the pages we will process
    return page_list


# iterate through all the pages and get all the cases
def get_cases(url):
    case_list = []
    # call the previous function to get all the URL pages
    page_list = get_pages(url)
    for page in page_list:
	
        # each page has a list of results, that is actually the list of cases, so we get the list and get each case out
        for result in page['results']:
            # append each case to the list of cases
            case_list.append(result)
    return case_list


def search_story(keyword):
    starting_url = 'https://api.case.law/v1/cases/?search=' + keyword

    results_count = 0

    # call previous function to get all the cases for the starting_url that is constructed above
    case_list = get_cases(starting_url)
    oldest_case = {}

    # go through each case
    for case in case_list:
        results_count += 1

        id = case['id']
        name = case['name_abbreviation']
        jurisdiction = case['jurisdiction']['name_long']
        date = case['decision_date']
        url = case['url']
        if ("date" not in oldest_case) or (oldest_case["date"] > date):
            oldest_case["id"] = id
            oldest_case["jurisdiction"] = jurisdiction
            oldest_case["date"] = date
            oldest_case["url"] = url+"?full_case=true&format=html"
            oldest_case["name"] = name

    print("there are ", results_count, "cases")
    print(oldest_case)

# here you enter the keyword to be searched. Use %20 for SPACE character
print("before")
search_story('El%20Chapo%20Guzman')
print("after")