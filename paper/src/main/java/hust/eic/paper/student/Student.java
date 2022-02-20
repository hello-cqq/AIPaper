package hust.eic.paper.student;

public class Student {

	String num;
	String name;
	String banji;
	Grade grade;
	public Student(String num, String name, String banji, Grade grade) {
		super();
		this.num = num;
		this.name = name;
		this.banji = banji;
		this.grade = grade;
	}
	public String getNum() {
		return num;
	}
	public void setNum(String num) {
		this.num = num;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getBanji() {
		return banji;
	}
	public void setBanji(String banji) {
		this.banji = banji;
	}

	public Grade getGrade() {
		return grade;
	}
	public void setGrade(Grade grade) {
		this.grade = grade;
	}
	@Override
	public String toString() {
		return "Student [num=" + num + ", name=" + name + ", banji=" + banji + ", grade=" + grade + "]";
	}
	
	
}
