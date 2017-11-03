from random import normalvariate as norm_dist
PERSONALITIES = {} # Dict of personality mu/sigma combos for OCEAN model
PERSONALITIES["balanced"] = {"O": [], "C": [], "E": [], "A": [], "N": []}
PERSONALITIES["engineer"] = {"O": [], "C": [], "E": [], "A": [], "N": []}
PERSONALITIES["designer"] = {"O": [], "C": [], "E": [], "A": [], "N": []}

# The OCEAN Model (from https://www.verywell.com/the-big-five-personality-dimensions-2795422)

# OPENNESS
# 
# This trait features characteristics such as imagination and insight, 
# and those high in this trait also tend to have a broad range of interests. 
# People who are high in this trait tend to be more adventurous and creative. 
# People low in this trait are often much more traditional and may struggle
# with abstract thinking.
# 
# People who are high on the openness continuum are typically:
# 
#     Very creative
#     Open to trying new things
#     Focused on tackling new challenges
#     Happy to think about abstract concepts
# 
# Those who are low on this trait:
# 
#     Dislike change
#     Do not enjoy new things
#     Resist new ideas
#     Not very imaginative
#     Dislikes abstract or theoretical concepts
PERSONALITIES["balanced"]["O"] = [0.5, 0.1]
PERSONALITIES["engineer"]["O"] = [0.7, 0.2]
PERSONALITIES["designer"]["O"] = [0.8, 0.1]

# CONSCIENTIOUSNESS
# 
# Standard features of this dimension include high levels of thoughtfulness, 
# with good impulse control and goal-directed behaviors. Highly conscientiousness 
# tend to be organized and mindful of details.
# 
# Those who are high on the conscientiousness continuum also tend to:
# 
#     Spend time preparing
#     Finish important tasks right away
#     Pay attention to details
#     Enjoy having a set schedule
# 
# People who are low in this trait tend to:
# 
#     Dislike structure and schedules
#     Make messes and not take care of things
#     Fail to return things or put them back where they belong
#     Procrastinate important tasks
#     Fail to complete the things they are supposed to do
PERSONALITIES["balanced"]["C"] = [0.5, 0.1]
PERSONALITIES["engineer"]["C"] = [0.6, 0.2]
PERSONALITIES["designer"]["C"] = [0.4, 0.2]

# EXTRAVERSION
# 
# Extraversion is characterized by excitability, sociability, talkativeness, 
# assertiveness, and high amounts of emotional expressiveness.
# People who are high in extraversion are outgoing and tend to gain energy in 
# social situations. People who are low in extraversion (or introverted) tend 
# to be more reserved and have to expend energy in social settings.
# 
# People who rate high on extraversion tend to:
#     Enjoy being the center of attention
#     Like to start conversations
#     Enjoy meeting new people
#     Have a wide social circle of friends and acquaintances
#     Find it easy to make new friends
#     Feel energized when they are around other people
#     Say things before they think about them
# 
# People who rate low on extraversion tend to:
#     Prefer solitude
#     Feel exhausted when they have to socialize a lot
#     Find it difficult to start conversations
#     Dislike making small talk
#     Carefully think things through before they speak
#     Dislike being the center of attention
PERSONALITIES["balanced"]["E"] = [0.5, 0.1]
PERSONALITIES["engineer"]["E"] = [0.2, 0.2]
PERSONALITIES["designer"]["E"] = [0.8, 0.2]

# AGREEABLENESS
# 
# This personality dimension includes attributes such as trust, altruism, 
# kindness, affection, and other prosocial behaviors. People who are high in 
# agreeableness tend to be more cooperative while those low in this trait tend
# to be more competitive and even manipulative.
# 
# People who are high in the trait of agreeableness tend to:
#     Have a great deal of interest in other people
#     Care about others
#     Feel empathy and concern for other people
#     Enjoy helping and contributing to the happiness of other people
# 
# Those who are low in this trait tend to:
#     Take little interest in others
#     Don't care about how other people feel
#     Have little interest in other people's problems
#     Insult and belittle others
PERSONALITIES["balanced"]["A"] = [0.5, 0.1]
PERSONALITIES["engineer"]["A"] = [0.3, 0.2]
PERSONALITIES["designer"]["A"] = [0.6, 0.2]

# NEUROTICISM
# 
# Neuroticism is a trait characterized by sadness, moodiness, and emotional
# instability. Individuals who are high in this trait tend to experience mood
# swings, anxiety, irritability and sadness. Those low in this trait tend to be
# more stable and emotionally resilient.
# 
# Individuals who are high in neuroticism tend to:
#     Experience a lot of stress
#     Worry about many different things
#     Get upset easily
#     Experience dramatic shifts in mood
#     Feel anxious
# 
# Those who are low in this trait are typically:
#     Emotionally stable
#     Deal well with stress
#     Rarely feel sad or depressed
#     Don't worry much
#     Very relaxed
PERSONALITIES["balanced"]["N"] = [0.5, 0.1]
PERSONALITIES["engineer"]["N"] = [0.7, 0.2]
PERSONALITIES["designer"]["N"] = [0.4, 0.1]

# Model each object on the big 5 OCEAN traits over a spectrum of [0, 1]
class Big5Model(object):
    def __init__(self, personality="balanced"):
        self.personality = personality
        
        limit = lambda f: max(min(f, 1.), 0.)
        self.O = limit(norm_dist(*PERSONALITIES[personality]["O"]))
        self.C = limit(norm_dist(*PERSONALITIES[personality]["C"]))
        self.E = limit(norm_dist(*PERSONALITIES[personality]["E"]))
        self.A = limit(norm_dist(*PERSONALITIES[personality]["A"]))
        self.N = limit(norm_dist(*PERSONALITIES[personality]["N"]))

    def __repr__(self):
        return "{}(personality='{}')".\
                format(self.__class__.__name__, self.personality)

    def __str__(self):
        return self.__repr__() + \
            " [O: {:0.2f}, C: {:0.2f}, E: {:0.2f}, A: {:0.2f}, N: {:0.2f}]".\
                    format(self.O, self.C, self.E, self.A, self.N)


if __name__ == '__main__':
    # Testing
    print(Big5Model())
    for _ in range(5):
        print(Big5Model(personality="balanced"))
    for _ in range(5):
        print(Big5Model(personality="engineer"))
    for _ in range(5):
        print(Big5Model(personality="designer"))
