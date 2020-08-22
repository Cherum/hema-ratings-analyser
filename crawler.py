from lxml import html
import requests
from enum import Enum
import sys, getopt

class ConfidenceLevel(Enum):
    HIGH = 1
    MEDIUM = 2
    ALL = 3

def isValidConfidence(minimalConfidenceLevel, confidence):
    if minimalConfidenceLevel == ConfidenceLevel.HIGH:
        return 'High' in confidence
    elif minimalConfidenceLevel == ConfidenceLevel.MEDIUM:
        matches = ['High', 'Medium']
        return any(x in confidence for x in matches)
    else:
        matches = ['High', 'Medium', 'Low', 'Inactive']
        return any(x in confidence for x in matches)

def addToClubRating(clubRatingDict, club, rating):
    if club not in clubRatingDict:
        clubRatingDict[club] = float(rating)
    else:
        clubRatingDict[club] += float(rating)

def addToClubMemberCount(clubMemberCountDict, club):
    if club not in clubMemberCountDict:
        clubMemberCountDict[club] = 1
    else:
        clubMemberCountDict[club] += 1

def buildAverageRating(clubMemberCountDict, clubRatingDict, memberCutOff):
    clubAverageRatingDict = {}
    for club in clubMemberCountDict:
        totalRating = clubRatingDict[club]
        memberCount = clubMemberCountDict[club]
        averageRating = totalRating / memberCount
        if memberCount >= memberCutOff:
            clubAverageRatingDict[club] = averageRating
    return clubAverageRatingDict

def printSortedResult(clubAverageRatingDict, clubMemberCountDict):
    print("Club (Counted Members): Average Rating")
    a1_sorted_keys = sorted(clubAverageRatingDict, key=clubAverageRatingDict.get, reverse=True)
    for r in a1_sorted_keys:
        print("{club} ({memberCount}): {averageRating}".format(club=r, memberCount=clubMemberCountDict[r], averageRating=round(clubAverageRatingDict[r], 2)))

def parsePageForClubs(requestUrl):
    page = requests.get(requestUrl)
    tree = html.fromstring(page.content)
    clubs = tree.xpath('//tbody/tr')
    return clubs

def main(argv):
    memberCutOff = 0
    minimalConfidenceLevel = ConfidenceLevel.ALL
    requestUrl = 'https://hemaratings.com/periods/details/?ratingsetid=1&nationality=de&year=2020&month=8'

    try:
        opts, args = getopt.getopt(argv,"hm:u:c:")
    except getopt.GetoptError as err:
        print ('error!', err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -u request url -m member cut off count -c minimal confidence level: high, medium or all')
            sys.exit()
        if opt == '-m':
            memberCutOff = int(arg)
        if opt == '-u':
            requestUrl = arg
        if opt == '-c':
            confString = arg.lower()
            if confString == 'high':
                minimalConfidenceLevel = ConfidenceLevel.HIGH
            elif confString == 'medium':
                minimalConfidenceLevel = ConfidenceLevel.MEDIUM
            elif confString == 'all':
                minimalConfidenceLevel = ConfidenceLevel.ALL
            else:
                print("Couldn't recognize confidence level:", arg)

    clubRatingDict = {}
    clubMemberCountDict = {}
    for entry in parsePageForClubs(requestUrl):
        club = ""
        rating = 0
        validConfidence = False
        for td in entry.getchildren():
            if(len(td.getchildren()) == 0):
                club = td.text.strip()
            else:
                isClubOrAthlete = td.find("a")
                isRating = td.find("span[@style]")
                if(isRating != None):
                    rating =  td.findtext("span")
                elif(isClubOrAthlete != None):
                    clubElement = td.xpath("a[contains(@href, '/clubs/')]")
                    if(len(clubElement) == 1):
                        club = clubElement[0].text

                if td.find("i") != None:
                    confidence = td.find('i').get("title")
                    validConfidence = isValidConfidence(minimalConfidenceLevel, confidence)

        if validConfidence:
            addToClubRating(clubRatingDict, club, rating)
            addToClubMemberCount(clubMemberCountDict, club)

    assert len(clubRatingDict) == len(clubMemberCountDict)  # both lists need to be of the same length

    clubAverageRatingDict = buildAverageRating(clubMemberCountDict, clubRatingDict, memberCutOff)
    printSortedResult(clubAverageRatingDict, clubMemberCountDict)

if __name__ == "__main__":
   main(sys.argv[1:])
