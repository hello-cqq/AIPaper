package hust.eic.paper.teacher;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;

public class Test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String str = "[{'first':'1'},{'first':'2'}]";
		JSONArray j = JSON.parseArray(str);
		System.out.println(j.getJSONObject(1).getString("first"));
	}

}
