module launch {

  import random;

  void launch_wave_around_area(object fgname,object faction,object type,object ai,int nr_ships,float r1,float r2,object pos){
    

    float x=_olist.at(pos,0)+(random.random(r1,r2)*random.randomsign());
    float y=_olist.at(pos,1)+(random.random(r1,r2)*random.randomsign());
    float z=_olist.at(pos,2)+(random.random(r1,r2)*random.randomsign());

     _io.printf("launching %d ships type=%s faction=%s around area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _io.message("game","all","launching new wave of fighters:");
    _io.message("game","all",type);

    _unit.launch(fgname,faction,type,ai,nr_ships,x,y,z);
  };


  void launch_wave_in_area(object fgname,object faction,object type,object ai,int nr_ships,float radius,object pos){

    float x=_olist.at(pos,0)+random.random((0.0-radius)/2.0,radius/2.0);
    float y=_olist.at(pos,1)+random.random((0.0-radius)/2.0,radius/2.0);
    float z=_olist.at(pos,2)+random.random((0.0-radius)/2.0,radius/2.0);

    _io.printf("launching %d ships type=%s faction=%s in area [%f,%f,%f]\n",nr_ships,type,faction,x,y,z);

    _io.message("game","all","launching new wave of fighters:");
    _io.message("game","all",type);

    _unit.launch(fgname,faction,type,ai,nr_ships,x,y,z);
  };
}
