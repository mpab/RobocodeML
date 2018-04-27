package Bots;

import robocode.*;

public class Random extends AdvancedRobot {

    private BotProxy proxy = new BotProxy(this);

    public void run() {
        while (true) {
            proxy.execRandomAction();
        }
    }

    public void onScannedRobot(ScannedRobotEvent e) {
        proxy.onScannedRobot(e);
    }

}
