package NN;

import robocode.*;

public class Random extends AdvancedRobot {

    private BotProxy proxy = new BotProxy(this);

    public void run() {
        while (true) {
            int action = proxy.randomAction();
            proxy.execAction(action);
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {
        proxy.fireAtEnemy(e.getDistance());
    }
}
