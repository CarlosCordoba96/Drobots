#include "drobots.ice"

module robots {
dictionary<int, Object*> ProxyDictionary;
sequence <int> attackerslist;
     interface Container {
         void link(int key, Object* proxy,string type);
         void unlink(int key);
         ProxyDictionary list();
         Object* getElementAt(int key);
         void setType(string type);
         string getType();
         attackerslist getAttackers();
     };
      sequence <drobots::Point> mines;

     interface ControllerFactory {
         drobots::RobotController* make(drobots::Robot* bot, Container* container, int key, mines minas,int nattackers);
     };

     interface DetectorControllerfactory {
     drobots::DetectorController* make(Container* Container);
     };

     interface RobotControllerAttacker extends drobots::RobotController {
         void allies(drobots::Point point, int id);
         void enemies(drobots::Point point);
     };
     exception IndexError{};

     interface RobotControllerDefender extends drobots::RobotController {
         void allies(drobots::Point point, int id);
     };

};
