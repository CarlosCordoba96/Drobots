#include "drobots.ice"

module robots {
dictionary<int, Object*> ProxyDictionary;

     interface Container {
         void link(int key, Object* proxy);
         void unlink(int key);
         ProxyDictionary list();
         Object* getElementAt(int key);
         void setType(string type);
         string getType();
     };
      sequence <drobots::Point> mines;

     interface ControllerFactory {
         drobots::RobotController* make(drobots::Robot* bot, Container* container, int key, mines minas);

     };

     interface DetectorControllerfactory {
     drobots::DetectorController* make(Container* Container);
  };

     interface RobotControllerAttacker extends drobots::RobotController {
         void setContainer(Container* container);
         void friendPosition(drobots::Point point, int id);
     };

     interface RobotControllerDefender extends drobots::RobotController {
         void setContainer(Container* container);
         void friendPosition(drobots::Point point, int id);
     };
};
