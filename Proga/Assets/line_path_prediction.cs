using System.Collections;
using System.Collections.Generic;
using System.Net.Http;
using UnityEngine;


public class Data {
    public double throttle { get; set; } 
    public double steering { get; set; } 
    public double brake { get; set; } 
    public bool handbrake { get; set; } 
    public bool is_manual_gear { get; set; } 
    public int manual_gear { get; set; } 
    public bool gear_immediate { get; set; } 
}


namespace HttpClientEx {
	public class line_path_prediction : MonoBehaviour
	{
		LineRenderer lr;
		public Transform car_position;
		public Transform mid_path_position;
		public Transform end_path_position;


		// public async void getRequest() {
		// 	using (var httpClient = new System.Net.Http.HttpClient()) {
		// 	    var json = await httpClient.GetStringAsync("http://127.0.0.1:5000/hub/getControl");
		// 	    Data data_obj = JsonConvert.DeserializeObject<Data >(json);
		// 	    Console.WriteLine(data_obj.steering);
		// 	}
		// }


	    void Start() {
	        lr = GetComponent<LineRenderer>();
	    }


	    void Update()
	    {

	    	// getRequest();
	    	

	    	lr.positionCount = 3;
	    	lr.SetPosition(0, car_position.position);
	    	lr.SetPosition(1, mid_path_position.position);
	        lr.SetPosition(2, end_path_position.position);
	    }
	}
}