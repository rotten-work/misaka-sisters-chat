import os
import random
import yaml
from PIL import Image

import language_unit
import sentiment_unit

if __name__ == "__main__":
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    # request_text = "你妈死了。"
    request_text = "你妈死了"
    print("Request text:")
    print(request_text)

    response = language_unit.get_chat_result(
        request_text, config['turing']['url'], config['turing']['key'])

    print("Before processing:")
    print(response)

    processed_resp = language_unit.post_process(response)
    
    print("After processing:")
    print(processed_resp)

    """ 你的 APPID AK SK """
    APP_ID = config['baidu']['app_id']
    API_KEY = config['baidu']['api_key']
    SECRET_KEY = config['baidu']['secret_key']

    sentiment_res = sentiment_unit.get_sentiment_result(response, str(APP_ID), API_KEY, SECRET_KEY)
    print(sentiment_res)

    # Parse sentiment result
    sentiment_items = sentiment_res['items']

    item = None
    for current_item in sentiment_items:
        if item is not None:
            if current_item['prob'] >= item['prob']:
                item = current_item
        else:
            item = current_item

    POSITIVE_MAIN_EMOTICONS_DIR_PATH = "emoticons/positive/main/"
    ANGRY_EMOTICONS_DIR_PATH = "emoticons/negative/angry/"

    def get_file_paths(dir):
        files = os.listdir(dir)
        paths = []
        for f in files:
            paths.append(os.path.join(dir, f))
        return paths

    positive_main_emoticon_paths = get_file_paths(POSITIVE_MAIN_EMOTICONS_DIR_PATH)
    angry_emoticon_paths = get_file_paths(ANGRY_EMOTICONS_DIR_PATH)
    
    # print(positive_main_emoticon_paths)
    # print(angry_emoticon_paths)

    prob = item['prob']
    label = item['label']
    subitems = item['subitems']

    postive_label = sentiment_unit.postive_label
    negative_label = sentiment_unit.negative_label

    prob_min_sentiment = 0.75
    prob_min_angry = 0.5

    random_emoticon_path = None
    if prob >= prob_min_sentiment:
        if label == postive_label:
            print("Show positive emoticon")
            random_emoticon_path = random.choice(positive_main_emoticon_paths)
        elif label == negative_label:
            for subitem in subitems:
                if (subitem['label'] == 'angry' and
                    subitem['prob'] >= prob_min_angry):
                    print("Show angry negative emoticon")
                    random_emoticon_path = random.choice(angry_emoticon_paths)
                    break

    if random_emoticon_path is not None:
        im = Image.open(random_emoticon_path)
        im.show()

    # min_value_to_show_postive_emoticon = 0.75
    # max_value_to_show_negative_emoticon = 0.25
    # sentiment_score = bx_predict(response)
    # # sentiment_score = bx_predict("开心不起来")
    # print(f"Sentiment score: {sentiment_score}")

    # if sentiment_score >= min_value_to_show_postive_emoticon:
    #     print("Show positive emoticon")
    # elif sentiment_score <= max_value_to_show_negative_emoticon:
    #     print("Show negative emoticon")