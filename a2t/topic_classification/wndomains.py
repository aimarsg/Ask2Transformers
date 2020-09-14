from typing import List

import numpy as np

from . import NLITopicClassifierWithMappingHead

WNDOMAINS_TOPICS = [
    "play",
    "tourism",
    "politics",
    "alimentation",
    "astrology",
    "biology",
    "history",
    "physics",
    "pedagogy",
    "color",
    "medicine",
    "psychology",
    "commerce",
    "fashion",
    "anthropology",
    "astronomy",
    "mathematics",
    "administration",
    "agriculture",
    "computer science",
    "earth",
    "law",
    "number",
    "archaeology",
    "literature",
    "time period",
    "quality",
    "engineering",
    "architecture",
    "veterinary",
    "military",
    "transport",
    "body care",
    "metrology",
    "industry",
    "chemistry",
    "telecommunication",
    "art",
    "sexuality",
    "sport",
    "religion",
    "person",
    "philosophy",
    "linguistics",
    "publishing",
    "artisanship",
    "sociology",
    "economy"
]

WNDOMAINS_TOPIC_MAPPING = {
    "acoustics": "physics",
    "administration": "administration",
    "aeronautic": "transport",
    "agriculture": "agriculture",
    "alimentation": "alimentation",
    "anatomy": "biology",
    "anthropology": "anthropology",
    "archaeology": "archaeology",
    "archery": "sport",
    "architecture": "architecture",
    "art": "art",
    "artisanship": "artisanship",
    "astrology": "astrology",
    "astronautics": "engineering",
    "astronomy": "astronomy",
    "athletics": "sport",
    "atomic physic": "physics",
    "auto": "transport",
    "badminton": "sport",
    "banking": "economy",
    "baseball": "sport",
    "basketball": "sport",
    "betting": "play",
    "biochemistry": "biology",
    "biology": "biology",
    "body care": "body care",
    "book keeping": "economy",
    "botany": "biology",
    "bowling": "sport",
    "boxing": "sport",
    "building industry": "architecture",
    "card": "play",
    "chemistry": "chemistry",
    "chess": "play",
    "cinema": "telecommunication",
    "color": "color",
    "commerce": "commerce",
    "computer science": "computer science",
    "cricket": "sport",
    "cycling": "sport",
    "dance": "art",
    "dentistry": "medicine",
    "diplomacy": "politics",
    "diving": "sport",
    "drawing": "art",
    "earth": "earth",
    "ecology": "biology",
    "economy": "economy",
    "electricity": "physics",
    "electronics": "physics",
    "electrotechnics": "engineering",
    "engineering": "engineering",
    "enterprise": "economy",
    "entomology": "biology",
    "ethnology": "anthropology",
    "exchange": "economy",
    "fashion": "fashion",
    "fencing": "sport",
    "fishing": "sport",
    "folklore": "anthropology",
    "football": "sport",
    "furniture": "architecture",
    "gas": "physics",
    "gastronomy": "alimentation",
    "genetics": "biology",
    "geography": "earth",
    "geology": "earth",
    "geometry": "mathematics",
    "golf": "sport",
    "grammar": "linguistics",
    "heraldry": "history",
    "history": "history",
    "hockey": "sport",
    "hunting": "sport",
    "hydraulics": "engineering",
    "industry": "industry",
    "insurance": "economy",
    "jewellery": "art",
    "law": "law",
    "linguistics": "linguistics",
    "literature": "literature",
    "mathematics": "mathematics",
    "mechanics": "engineering",
    "medicine": "medicine",
    "merchant navy": "transport",
    "meteorology": "earth",
    "metrology": "metrology",
    "military": "military",
    "money": "economy",
    "mountaineering": "sport",
    "music": "art",
    "mythology": "religion",
    "number": "number",
    "numismatics": "art",
    "occultism": "religion",
    "oceanography": "earth",
    "optics": "physics",
    "painting": "art",
    "paleontology": "earth",
    "pedagogy": "pedagogy",
    "person": "person",
    "pharmacy": "medicine",
    "philately": "art",
    "philology": "literature",
    "philosophy": "philosophy",
    "photography": "art",
    "physics": "physics",
    "physiology": "biology",
    "plastic arts": "art",
    "play": "play",
    "politics": "politics",
    "post": "telecommunication",
    "psychiatry": "medicine",
    "psychoanalysis": "psychology",
    "psychology": "psychology",
    "publishing": "publishing",
    "quality": "quality",
    "racing": "sport",
    "radio": "telecommunication",
    "radiology": "medicine",
    "railway": "transport",
    "religion": "religion",
    "roman catholic": "religion",
    "rowing": "sport",
    "rugby": "sport",
    "school": "pedagogy",
    "sculpture": "art",
    "sexuality": "sexuality",
    "skating": "sport",
    "skiing": "sport",
    "soccer": "sport",
    "sociology": "sociology",
    "sport": "sport",
    "statistics": "mathematics",
    "sub": "sport",
    "surgery": "medicine",
    "swimming": "sport",
    "table tennis": "sport",
    "tax": "economy",
    "telecommunication": "telecommunication",
    "telegraphy": "telecommunication",
    "telephony": "telecommunication",
    "tennis": "sport",
    "textiles": "industry",
    "theatre": "art",
    "theology": "religion",
    "time period": "time period",
    "topography": "astronomy",
    "tourism": "tourism",
    "town planning": "architecture",
    "transport": "transport",
    "tv": "telecommunication",
    "university": "pedagogy",
    "veterinary": "veterinary",
    "volleyball": "sport",
    "wrestling": "sport",
    "zoology": "biology",
    "zootechnics": "veterinary"
}


class WNDomainsClassifier(NLITopicClassifierWithMappingHead):
    """ WNDomainsClassifier

    Specific class for topic classification using WNDomains topic set.
    """

    def __init__(self, **kwargs):
        super(WNDomainsClassifier, self).__init__(
            pretrained_model='roberta-large-mnli', topics=WNDOMAINS_TOPICS, topic_mapping=WNDOMAINS_TOPIC_MAPPING,
            query_phrase="The domain of the sentence is about", entailment_position=2, **kwargs)

        def idx2topic(idx):
            return WNDOMAINS_TOPICS[idx]

        self.idx2topic = np.vectorize(idx2topic)

    def predict_topics(self, contexts: List[str], batch_size: int = 1, return_labels: bool = True,
                       return_confidences: bool = False, topk: int = 1):
        output = self(contexts, batch_size)
        topics = np.argsort(output, -1)[:, ::-1][:, :topk]
        if return_labels:
            topics = self.idx2topic(topics)
        if return_confidences:
            topics = np.stack((topics, np.sort(output, -1)[:, ::-1][:, :topk]), -1).tolist()
            topics = [[(int(label), conf) if not return_labels else (label, conf) for label, conf in row]
                      for row in topics]
        else:
            topics = topics.tolist()
        if topk == 1:
            topics = [row[0] for row in topics]

        return topics
