intro_string="Have you heard of the Interplanetary Socialist Organization? We are a revolutionary organization trying to rid the Star Confederacy of its tired oligarchy. We are here to defend the rights of the poor workers! We are here to cause the downfall of the bourgeoise and enable the rise of the proletariat!"

import Base
import fixers
import Director
def AssignMission ():
	fixers.DestroyActiveButtons ()
	fixers.CreateChoiceButtons(Base.GetCurRoom(),[
		fixers.Choice("bases/fixers/yes.spr","bases/fixers/iso_mission.py","Accept This Agreement"),
		fixers.Choice("bases/fixers/no.spr","bases/fixers/iso_decline.py","Decline This Agreement")])

playa = VS.getPlayer();
playernum = playa.isPlayerStarship()
len=Director.getSaveDataLength (playernum,"kills");
kills=0
if (len!=0):
	kills=Director.getSaveData(playernum,"kills",len-1)
if (kills<0):
	Base.Message("Hello Pilot. " + intro_string + " We are actively seeking new members in our organization.  However to fly defense runs, you need some more experience. Come back when your record is somewhat more interesting and then together we can overthrow the confederacy!");
elif (VS.numActiveMissions()>1):
	Base.Message ("It is a pleasure to speak to you; however, if you wish to work with me you must first finish up your other contractual obligations.")
else:
	if (fixers.checkSaveValue (playernum,"iso_mission1",0)):
		Base.Message("Hello Mercenary. " + intro_string + " We are actively seeking mercenaries to help us defend our supplies and our party members.  There is a precious in this system vessel carrying several key party members and some valuable sensor data with them.  We offer 18000 credits if you will defend these starships, comrade! Do you accept our offer?")
#And then if you fail.......
		AssignMission()
	elif (fixers.checkSaveValue (playernum,"iso_mission1",-1)):
		Base.Message ("You conspirator! I should have realized you were a kepitalizt pig when I first smelled our foul stench! You probably got paid to destroy our vessel. If I shared in your lack of honor I would kill you where you stand.  But instead I shall ask my operatives to rid you of your ship. Fly you fool! Fly if you wish to have any shred of your starship left!")
		fixers.setSaveValue (playernum,"decided_iso_evil",1)
		type = faction_ships.getRandomFighter ("ISO")
		fgname="Lenin'sRevenge"
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		type = faction_ships.getRandomFighter ("ISO")
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
		launch.launch_wave_around_unit (fgname,"ISO",type,"default",1,80,300,playa).SetTarget(playa)
	elif (fixers.checkSaveValue (playernum,"iso_mission2",-1) or fixers.checkSaveValue (playernum,"iso_mission3",-1) or fixers.checkSaveValue (playernum,"iso_mission4",-1)):
		Base.Message ("You have failed the ISO.  I should have known not to entrust a self serving mercenary with the key plans of our organization. Go now... make money for yourself--I know you do not care for the peoples future.")
	else:
		if (fixers.checkSaveValue (playernum,"iso_mission1",1) and fixers.checkSaveValue(playernum,"iso_mission2",0)):			
			Base.Message ("Thank you for your help in defending our starship.  We had no idea that confed was on to us there.  I do believe it is not safe so far away from the defiance sector.  We have a starship in urgent need of escort.  It is a small, speedy merchant vessel that hopefully will slip past confeds defenses.  We have programmed its flight computer to follow you through jump points and to autopilot to your destination when you press the 'a' key.  Its final destination is the Adams sector; however, be wary that such a small ship will have trouble navigating throug the black hole in Enigma sector, so I have suggested an alternate route that will take you trhough a few backwater systems to adams.  Will you assist us?")#assign mis 2
			AssignMission()
		elif (fixers.checkSaveValue (playernum,"iso_mission2",1) and fixers.checkSaveValue(playernum,"iso_mission3",0)):			
			Base.Message ("Thank you for the escort kind comrade. I was personally aboard that starship, and I am quite relieved to be here in one piece.  However we have another job we'd like you to help us with.  This time the reward is quite sizable.  We have some rather...shady... cargo that needs transportation to our home system in Defiance.  We will offer you 20000 for this milk run. Will you do it?  If so I shall meet you there myself.")#assign mis 3:
			AssignMission()
		elif (fixers.checkSaveValue (playernum,"iso_mission3",1) and fixers.checkSaveValue(playernum,"iso_mission4",0)):
			Base.Message ("Thank you for a hasty delivery of the cargo.  However, we have an urgent problem here--there is a large confed assault on one of our assets here in Defiance. Can you help us stave them off? The revolution is getting quite out of hand, yet Confed thinks it still owns defiance even though not a living comrade here would raise arms for them.  With rulers like this how can Confed claim itself a democracy! It's outrageous! Will you help us?")#assign mis 4
			AssignMission()
		elif (fixers.checkSaveValue(playernum,"iso_mission4",1)):
			Base.Message ("You have helped the ISO when we have needed it. Your talent and dedication shall not be forgotten. They will be sung of in revolution and written in epics.  Thank you kind Socialist. You have earned your name as a man of the people.")
		else:
			Base.Message ("Make haste for the people! Tardiness is the opium for the masses!") 
