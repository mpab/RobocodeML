package NN;

import Common.Observation;
import org.json.JSONObject;

public class Tester extends Trainer {

    public void run() {

        conn.open("localhost", 8889);
        int frame = 1;

        obs = new Observation(getRoundNum() + 1, getNumRounds(), frame++, 0);
        conn.send(obs.toJson().toString());

        while (true) {
            int action = getNextAction();
            proxy.execAction(action);
            obs = new Observation(getRoundNum() + 1, getNumRounds(), frame++, 0);
            conn.send(obs.toJson().toString());
        }
    }

    private int getNextAction() {
        String msg = conn.receive();
        JSONObject jsn = new JSONObject(msg);
        int action = jsn.getInt("action");
        //System.out.printf("getNextAction() -> %s\n", proxy.actionToString(action));
        return action;
    }
}
