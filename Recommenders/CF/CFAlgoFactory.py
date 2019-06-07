from Recommenders.CF.CFItemBased import CFItemBased
from Recommenders.CF.CFUserBased import CFUserBased
class CFAlgoFactory():
	@staticmethod
	def get_cf_algo(sim_options):
		if sim_options['user_based'] == True:
			return CFUserBased()
		else:
			return CFItemBased()