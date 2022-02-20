package hust.eic.paper.course;

public class Course {

	int id;
	String name;
	String term;
	
	public Course(int id, String name, String term) {
		this.id = id;
		this.name = name;
		this.term = term;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getTerm() {
		return term;
	}

	public void setTerm(String term) {
		this.term = term;
	}

	@Override
	public String toString() {
		return "Course [id=" + id + ", name=" + name + ", term=" + term + "]";
	}
	
}
