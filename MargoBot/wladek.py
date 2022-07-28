from MargoBot.BotKlasy.bot_e2_class import BotE2
from MargoBot.KordyMap.podmokla_dolina_module import podmokla_dolina

postac = BotE2("", "", "")
postac.bij_e2("npc207678", 240, [10, 13], podmokla_dolina)
