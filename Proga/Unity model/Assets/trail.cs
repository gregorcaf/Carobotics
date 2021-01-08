using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class trail : MonoBehaviour
{

	private int status = 0;
	private bool shown = false;
	TrailRenderer tr;


    void Start()
    {
        tr = GetComponent<TrailRenderer>();
        tr.startColor = Color.red;
        tr.endColor = Color.blue;
        
    }

    // Update is called once per frame
    void Update() {
		status++;
        if (status == 100) {
            shown = !shown;
            status = 0;
        }

        if (shown) {
	        tr.startColor = Color.red;
        	tr.endColor = Color.blue;
    	} else {
	        tr.startColor = Color.blue;
        	tr.endColor = Color.red;
    	}
    }
}
