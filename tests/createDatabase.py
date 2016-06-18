from uplink.models import Generation, Rank, Merit, Division
from uplink.models import Personnel
from uplink.models import PersonnelAccount, PersonnelEnlistment, PersonnelMerit

def create_database(db):
	# Insert Ranks
	db.session.add(Rank('Rank I', 'Rank Description', '1e622479-e63c-4c3f-a9db-0cad702cdad7'))
	# Insert Divisions
	db.session.add(Division('The Division', 'Apparently disappointing', '81db5305-57ed-4fd0-b462-390a3b724ad8'))

	# Insert Generations
	db.session.add(Generation('The Generation', 'The first and only', '9da60769-3d4b-49ea-a942-b93d06e21adc'))

	# Insert Merits
	db.session.add(Merit('One Year of Service', 'Awarded to Personnel who have completed one year of service.', '444e5c09-d5bb-419f-95ce-2c805d35b816'))

	db.session.add(Personnel(2, True, rankID=1, divisionID=1))
	
	# PersonnelPersonnelAccounts
	db.session.add(PersonnelAccount(2, 'e37adbcf-dfa1-4cea-9ae7-5c25856327d7', 'main.resident', 'Main Resident', 'Main'))
	db.session.add(PersonnelAccount(2, 'a5904a08-57b1-48e7-9ab3-f93e831153e7', 'alt.resident', 'Alt Resident', 'Alt'))
	

	db.session.add(PersonnelEnlistment(1, '2016-06-20 04:00:00', 1))
	
	db.session.add(PersonnelMerit(1, 1, '2015-03-01 04:00:00', 'Awarded to Subzidion Nightfire for 5 Years of Service.'))
