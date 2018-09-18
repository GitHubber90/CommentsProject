import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='FhsLDLLcaCaB8g',
                     client_secret='62NK7J7RzqRJYUXf2gwhtLT91Mg',
                     user_agent='my user agent'
                     )
negative_comments_list = []
positive_comments_list=[]
neutral_comments_list=[]


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
   return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
   return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
   return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)

    return submission.comments



def process_comments(comments,positive_comments_list,negative_comments_list,neutral_comments_list):
    #These are all my probabilities for a single comment so this code will check how likely for the comment to be negative
    #These proba scanners are not perfect so many comments are not catagorized correctly
    positive_comment_proba = get_text_neutral_proba(comments.body)
    negative_comment_proba = get_text_negative_proba(comments.body)
    neutral_comment_proba = get_text_neutral_proba(comments.body)
    #A comment is positive if its positive proa(or probability) is higher thatn its negative
    #and also bigger than .5
    if positive_comment_proba > negative_comment_proba and positive_comment_proba >.5:
        positive_comments_list.append(comments.body)
    #A comment is negative if its negative proba exceeds the positive aswell as the neutral
    elif negative_comment_proba > positive_comment_proba and negative_comment_proba>neutral_comment_proba:
        negative_comments_list.append(comments.body)
    #If its not negative or positive it must be neutral
    else:
        neutral_comments_list.append(comments.body)

    for comment in comments.replies:
        #recursion here!
        process_comments(comment,positive_comments_list,negative_comments_list,neutral_comments_list)




def main():
    #TESTS/ be sure to only have one uncommented
    #comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    #comments = get_submission_comments('https://www.reddit.com/r/funny/comments/9gp4mr/do_you_think_he_likes_the_song/')
    comments = get_submission_comments('https://www.reddit.com/r/politics/comments/9gqhzr/if_you_see_disinformation_ahead_of_the_midterms/')
    for comment in comments:
        process_comments(comment,positive_comments_list,negative_comments_list,neutral_comments_list)
    #Prints all the lists
    print('---------------------------POSITIVE COMMENTS--------------------------------------')
    print(*positive_comments_list, sep = "\n")
    print('-------------------------------------------------------------------------NEGATIVE COMMENTS-------------------------------------------------------------')
    print(*negative_comments_list, sep="\n")
    print('-------------------------------------------------------------------------NEUTRAL COMMENTS-------------------------------------------------------------')
    print(*neutral_comments_list, sep="\n")
main()

