package hust.eic.paper;

import com.alibaba.fastjson.JSONObject;

public class Paper {

	int courseId;
	int total;
	JSONObject choice;
	JSONObject fill;
	JSONObject judge;
	JSONObject q_short;
	JSONObject q_compute;
	public Paper(int courseId, int total, JSONObject choice, JSONObject fill, JSONObject judge, JSONObject q_short,
			JSONObject q_compute) {
		super();
		this.courseId = courseId;
		this.total = total;
		this.choice = choice;
		this.fill = fill;
		this.judge = judge;
		this.q_short = q_short;
		this.q_compute = q_compute;
	}
	public int getCourseId() {
		return courseId;
	}
	public void setCourseId(int courseId) {
		this.courseId = courseId;
	}
	public int getTotal() {
		return total;
	}
	public void setTotal(int total) {
		this.total = total;
	}
	public JSONObject getChoice() {
		return choice;
	}
	public void setChoice(JSONObject choice) {
		this.choice = choice;
	}
	public JSONObject getFill() {
		return fill;
	}
	public void setFill(JSONObject fill) {
		this.fill = fill;
	}
	public JSONObject getJudge() {
		return judge;
	}
	public void setJudge(JSONObject judge) {
		this.judge = judge;
	}
	public JSONObject getQ_short() {
		return q_short;
	}
	public void setQ_short(JSONObject q_short) {
		this.q_short = q_short;
	}
	public JSONObject getQ_compute() {
		return q_compute;
	}
	public void setQ_compute(JSONObject q_compute) {
		this.q_compute = q_compute;
	}
	@Override
	public String toString() {
		return "Paper [courseId=" + courseId + ", total=" + total + ", choice=" + choice + ", fill=" + fill + ", judge="
				+ judge + ", q_short=" + q_short + ", q_compute=" + q_compute + "]";
	}
	
	
}
