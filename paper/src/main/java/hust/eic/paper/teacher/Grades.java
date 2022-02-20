package hust.eic.paper.teacher;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.alibaba.fastjson.JSONArray;

public class Grades {

}
class Choice{
	int[] goal;
	JSONArray answer;
	int grade;
	
	public Choice(int[] goal, JSONArray answer, int grade) {
		super();
		this.goal = goal;
		this.answer = answer;
		this.grade = grade;
	}
	
	public int getGrade() {
		return grade;
	}

	public void setGrade(int grade) {
		this.grade = grade;
	}

	public int[] getGoal() {
		return goal;
	}
	public void setGoal(int[] goal) {
		this.goal = goal;
	}
	public JSONArray getAnswer() {
		return answer;
	}
	public void setAnswer(JSONArray answer) {
		this.answer = answer;
	}

	@Override
	public String toString() {
		return "Choice [goal=" + Arrays.toString(goal) + ", answer=" + answer + ", grade=" + grade + "]";
	}
	
	
}
class Fill{
	
}
class Judge{
	double[] goal;
	double grade;
	String answer;
	public Judge(double[] goal, double grade, String answer) {
		super();
		this.goal = goal;
		this.grade = grade;
		this.answer = answer;
	}
	public double[] getGoal() {
		return goal;
	}
	public void setGoal(double[] goal) {
		this.goal = goal;
	}
	public double getGrade() {
		return grade;
	}
	public void setGrade(double grade) {
		this.grade = grade;
	}
	public String getAnswer() {
		return answer;
	}
	public void setAnswer(String answer) {
		this.answer = answer;
	}
	@Override
	public String toString() {
		return "Judge [goal=" + Arrays.toString(goal) + ", grade=" + grade + ", answer=" + answer + "]";
	}
	
	
}
class QShort{
	double[] goal;
	double grade;
	String answer;
	public QShort(double[] goal, double grade, String answer) {
		super();
		this.goal = goal;
		this.grade = grade;
		this.answer = answer;
	}
	public double[] getGoal() {
		return goal;
	}
	public void setGoal(double[] goal) {
		this.goal = goal;
	}
	public double getGrade() {
		return grade;
	}
	public void setGrade(double grade) {
		this.grade = grade;
	}
	public String getAnswer() {
		return answer;
	}
	public void setAnswer(String answer) {
		this.answer = answer;
	}
	@Override
	public String toString() {
		return "QShort [goal=" + Arrays.toString(goal) + ", grade=" + grade + ", answer=" + answer + "]";
	}
	
}
class QCompute{
	double grade;
	List<ComputeAns> answer = new ArrayList<ComputeAns>();
	public QCompute(double grade, List<ComputeAns> answer) {
		super();
		this.grade = grade;
		this.answer = answer;
	}
	public double getGrade() {
		return grade;
	}
	public void setGrade(double grade) {
		this.grade = grade;
	}
	public List<ComputeAns> getAnswer() {
		return answer;
	}
	public void setAnswer(List<ComputeAns> answer) {
		this.answer = answer;
	}
	@Override
	public String toString() {
		return "QCompute [grade=" + grade + ", answer=" + answer + "]";
	}
	
	
	
}

class ComputeAns{
	double goal;
	String path;
	public ComputeAns(double goal, String path) {
		super();
		this.goal = goal;
		this.path = path;
	}
	public double getGoal() {
		return goal;
	}
	public void setGoal(double goal) {
		this.goal = goal;
	}
	public String getPath() {
		return path;
	}
	public void setPath(String path) {
		this.path = path;
	}
	@Override
	public String toString() {
		return "ComputeAns [goal=" + goal + ", path=" + path + "]";
	}
	
}
