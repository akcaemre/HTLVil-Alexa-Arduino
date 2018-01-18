package data;

public class Room {
	private String name = "";
	private boolean isOn = false;
	
	public Room(String name, boolean isOn) {
		this.name = name;
		this.isOn = isOn;
	}

	public String getName() {
		return this.name;
	}

	public boolean isOn() {
		return this.isOn;
	}
	
	public void setIsOn(boolean newState) {
		this.isOn = newState;
	}

	@Override
	public String toString() {
		return "Im " + this.name + " ist das Licht " + (this.isOn ? "ein." : "aus.");
	}
}
