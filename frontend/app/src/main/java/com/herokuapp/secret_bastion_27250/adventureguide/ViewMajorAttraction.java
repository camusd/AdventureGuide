package com.herokuapp.secret_bastion_27250.adventureguide;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;


public class ViewMajorAttraction extends ActionBarActivity {

//    public static final String URL = "http://assign32ws-schmicar.rhcloud.com/ws/del_todo/";
    public static final String MY_PREFS = "MyPrefsFile";
    String name;
    String desc;
    Bitmap image;
    String id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_major_attraction);

        // get extras from intent and populate view
        Intent myIntent = getIntent();
        name = myIntent.getStringExtra("name");
        desc = myIntent.getStringExtra("desc");
        image = myIntent.getParcelableExtra("image");
        id = myIntent.getStringExtra("id");

        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theUser = prefs.getString("username", null);
        String theId = prefs.getString("id", null);

        TextView tv_name = (TextView)findViewById(R.id.adventure_guide_detail_name);
        TextView tv_desc = (TextView)findViewById(R.id.adventure_guide_detail_desc);
        ImageView iv_image = (ImageView)findViewById(R.id.imageView2);

        tv_name.setText(name);
        tv_desc.setText(desc);
        iv_image.setImageBitmap(image);

        Button button_write_review = (Button)findViewById(R.id.button9);

        if (theUser != null && !theUser.isEmpty()) {
            button_write_review.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_view_major_attraction, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 0) {
            recreate();
        }

    }

    public void readReviews(View view) {
        Intent intent = new Intent(this, ViewReviews.class);
        intent.putExtra("attraction", id);
        intent.putExtra("name", name);
        startActivityForResult(intent, 0);
    }

    public void writeReview(View view) {
        Intent intent = new Intent(this, WriteReview.class);
        intent.putExtra("attraction", id);
        intent.putExtra("review_name", name);
        startActivityForResult(intent, 0);
    }
}