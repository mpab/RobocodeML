package NN;

import Common.Observation;
import org.json.JSONObject;

public class NNTester extends NNTrainer {

    public void run() {

        conn.open("localhost", 8889);
        frame = 0;

        newObservation();
        conn.send(obs.toJson().toString()); // ensure we get an update

        while (true) {
            newObservation();
            int action = getNextAction();
            proxy.execAction(action);
            conn.send(obs.toJson().toString());
        }
    }

    private void newObservation() {
        Observation nobs = new Observation(getRoundNum() + 1, getNumRounds(), frame++, 0);
        nobs.action = -1;
        nobs.x = getX();
        nobs.y = getY();
        nobs.heading = getHeading();
        nobs.scanned_enemy_distance = lastEnemyDistance;
        nobs.scanned_enemy_bearing = lastEnemyBearing;
        nobs.scanned_enemy_x = lastEnemyX;
        nobs.scanned_enemy_y = lastEnemyY;
        obs = nobs;
    }

    private int getNextAction() {
        String msg = conn.receive();
        JSONObject jsn = new JSONObject(msg);
        int action = jsn.getInt("action");
        //System.out.printf("getNextAction() -> %s\n", proxy.actionToString(action));
        return action;
    }


}
