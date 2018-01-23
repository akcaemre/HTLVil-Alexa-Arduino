package data;

import java.awt.BorderLayout;
import java.awt.Color;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;

import javax.swing.*;

public class ProtocolMonitorMain extends JFrame{

	private static final long serialVersionUID = 1L;
		
	private static JLabel header;
	private static JTextArea mainOutput;
	
	private static String SEPERATOR = ";";
	
	public static void main(String[] args) {
		header = new JLabel("Protokoll der Sprachein- und Sprachausgaben");
		mainOutput = new JTextArea("\n" + getTimeStamp() + "Started.");
		mainOutput.setEditable(false);
		
		// initializes this frame
		ProtocolMonitorMain m = new ProtocolMonitorMain();
		m.setTitle("ALEXA Skill protokollierung");
	    m.setSize(1070, 534);
	    m.setLayout(new BorderLayout());
	    m.setBackground(Color.CYAN);
	    
	    m.add(header, BorderLayout.NORTH);
	    m.add(mainOutput, BorderLayout.CENTER);
	    
	    m.setVisible(true);
		
		BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));

		try {
			String s = bufferRead.readLine();
	
			while(!s.equals("x")) {
				String[] splitted = s.split(SEPERATOR);
				
				if(splitted.length > 1) {
					String userText = splitted[0];
					String alexaText = splitted[1];
					
					String output = "\n" + getTimeStamp() + userText 
									+ "\n" + getTimeStamp() + alexaText 
									+ "\n\n" + mainOutput.getText() ;
					
					mainOutput.setText(output);
					
					m.repaint();
				}
				
				s = bufferRead.readLine();
			}
		}
		catch (Exception e) { e.printStackTrace(); }
	}

	private static String getTimeStamp() {
		return "<" + new SimpleDateFormat("HH:mm:ss").format(new Date()) + "> ";
	}	
}
