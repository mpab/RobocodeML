package Bots;

import java.io.*;
import java.net.*;

public class Connection {

    int battle;
    int maxBattles;

    Socket socket = null;

    public void open(int battle, int maxBattles) {
        try {
            if (socket == null) {
                socket = new Socket("localhost", 8888);
                this.battle = battle + 1;
                this.maxBattles = maxBattles;
            }
        } catch(Exception e) {
            System.out.println(e);
            socket = null;
        }
    }

    public boolean isOpen() {
        return socket != null;
    }

    public void close() {
        if (socket != null) {
            try {
                socket.close();
            } catch(Exception e) {
                System.out.println(e);
            }
            socket = null;
        }
    }

    public void send(String k, String v) {
        if (isOpen()) {
            String msg = String.format("'%d/%d':'%s':'%s'", battle, maxBattles, k, v);
            send(msg);
        }
    }

    public void send(String msg) {
        if (isOpen()) {
            try {
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                out.writeUTF(msg);
                //out.writeUTF("");
                out.flush();
            } catch (Exception e) {
                System.out.println(e);
                close();
            }
        }
    }
}
