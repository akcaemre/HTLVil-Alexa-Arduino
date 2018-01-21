package data;

import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.URL;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Main extends JFrame {
	private static final long serialVersionUID = 8401140811597166481L;
	
	private static ArrayList<Room> rooms = new ArrayList<Room>();
	
	private static final String SEPERATOR = ":";
	private static String backgroundURL 	= "https://www.dropbox.com/s/6suycpeg3vyp60y/smarthome_dark.jpg?dl=1";
	private static String bathroomURL 	= "https://www.dropbox.com/s/um7g7aoor6n149y/Bad.png?dl=1";
	private static String bedroomURL 	= "https://www.dropbox.com/s/8aou7r3l7f7osfx/Schlafzimmer.png?dl=1";
	private static String garageURL 		= "https://www.dropbox.com/s/g98kezt5vqoyrx5/Garage.png?dl=1";
	private static String kitchenURL 	= "https://www.dropbox.com/s/psxrh3fihjs7l5e/K%C3%BCche.png?dl=1";
	private static String livingroomURL 	= "https://www.dropbox.com/s/egs69l8dndogxxq/Wohnzimmer.png?dl=1";

	private static URL urlImageBackground;
	private static URL urlImageBathroom;
	private static URL urlImageBedroom;
	private static URL urlImageGarage;
	private static URL urlImageKitchen;
	private static URL urlImageLivingroom;
	
	private static Image backgroundImage;
	private static Image bathroomImage;
	private static Image bedroomImage;
	private static Image garageImage;
	private static Image kitchenImage;
	private static Image livingroomImage;
    
	private static BufferedImage finalImage;
	
	private static Graphics2D g;
	
	private static JPanel gui;
	
	private static int w, h;
	
	public static void main(String[] args) {
			try {
				// -- Initialize phase --
				rooms.add(new Room("wohnzimmer", false));
				rooms.add(new Room("küche", false));
				rooms.add(new Room("schlafzimmer", false));
				rooms.add(new Room("bad", false));
				rooms.add(new Room("garage", false));

				urlImageBackground = new URL(backgroundURL);
				urlImageBathroom = new URL(bathroomURL);
				urlImageBedroom = new URL(bedroomURL);
				urlImageGarage = new URL(garageURL);
				urlImageKitchen = new URL(kitchenURL);
				urlImageLivingroom = new URL(livingroomURL);
				
			    backgroundImage = ImageIO.read(urlImageBackground);
			    bathroomImage = ImageIO.read(urlImageBathroom);
			    bedroomImage = ImageIO.read(urlImageBedroom);
			    garageImage = ImageIO.read(urlImageGarage);
			    kitchenImage = ImageIO.read(urlImageKitchen);
			    livingroomImage = ImageIO.read(urlImageLivingroom);
			    
			    w = backgroundImage.getWidth(null);
			    h = backgroundImage.getHeight(null);
			    
			    finalImage = new BufferedImage(w, h, BufferedImage.TYPE_INT_RGB);

			    gui = new JPanel(new GridLayout(1, 0, 1, 1));
			    
			    refreshUI();
			    
		        gui.add(new JLabel(new ImageIcon(finalImage)));
		        
			    Main m = new Main();
			    m.setSize(1070, 534);
				m.add(gui);
			    m.setVisible(true);
				
				BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));

				String s = bufferRead.readLine();

				while(!s.equals("x")) {
					if(s.startsWith("TurnOn" + SEPERATOR)) {
						String[] splitted = s.split(SEPERATOR);
						
						if(splitted.length > 1) {
							Room r = findRoomByName(splitted[1].toLowerCase());
							
							if(r != null)
								r.setIsOn(true);
						}
					} else if(s.startsWith("TurnOff" + SEPERATOR)) {
						String[] splitted = s.split(SEPERATOR);
						
						if(splitted.length > 1) {
							Room r = findRoomByName(splitted[1].toLowerCase());
							
							if(r != null)
								r.setIsOn(false);
						}
					} else if(s.equals("TurnOnAll")) {
						for (Room r : rooms)
							r.setIsOn(true);
					} else if(s.equals("TurnOffAll")) {
						for (Room r : rooms)
							r.setIsOn(false);
					}
					
					refreshUI();
					
					s = bufferRead.readLine();
				}
			} catch (Exception e) { e.printStackTrace(); }
	}
	
	private static void refreshUI() {
		g = finalImage.createGraphics();
		
		g.clearRect(0, 0, w, h);

	    g.drawImage(backgroundImage, 0, 0, null);
	    
	    if(findRoomByName("bad").isOn()) g.drawImage(bathroomImage, 45, 155, null);
	    if(findRoomByName("schlafzimmer").isOn()) g.drawImage(bedroomImage, 325, 155, null);
	    if(findRoomByName("garage").isOn()) g.drawImage(garageImage, 700, 330, null);
	    if(findRoomByName("küche").isOn()) g.drawImage(kitchenImage, 415, 330, null);
	    if(findRoomByName("wohnzimmer").isOn()) g.drawImage(livingroomImage, 45, 330, null);
	    
	    g.dispose();
	    
	    gui.repaint();
	}
	
	private static Room findRoomByName(String roomName) {
		for(Room r : rooms) 
			if(r.getName().equals(roomName))
				return r;
		
		return null;
	}
}
