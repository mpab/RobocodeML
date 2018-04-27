package Bots;

import java.io.*;
import java.net.*;
import org.json.*;

public class Connection {

    Socket socket = null;

    public void open() {

        if (isOpen())
            return;

        try {
            if (socket == null) {
                socket = new Socket("localhost", 8888);
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

    public void send(String msg) {
        if (isOpen()) {
            try {
                DataOutputStream out = new DataOutputStream(socket.getOutputStream());
                out.writeBytes(msg);
                out.flush();
            } catch (Exception e) {
                System.out.println(e);
                close();
            }
        }
    }
}
