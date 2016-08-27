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
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;


public class ViewReview extends ActionBarActivity {

    public static final String URL = "http://secret-bastion-27250.herokuapp.com/api/reviews/";
    public static final String MY_PREFS = "MyPrefsFile";
    String username;
    String body;
    String id;
    String attraction;
    String review_name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_review);

        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theUser = prefs.getString("username", null);
        String theId = prefs.getString("id", null);

        // get extras from intent and populate view
        Intent myIntent = getIntent();
        username = myIntent.getStringExtra("username");
        body = myIntent.getStringExtra("body");
        id = myIntent.getStringExtra("id");
        attraction = myIntent.getStringExtra("attraction");
        review_name = myIntent.getStringExtra("review_name");

        TextView tv_user = (TextView)findViewById(R.id.adventure_guide_detail_user);
        TextView tv_body = (TextView)findViewById(R.id.adventure_guide_detail_body);
        Button button_edit = (Button)findViewById(R.id.button10);
        Button button_delete = (Button)findViewById(R.id.button11);

        tv_user.setText(username);
        tv_body.setText(body);

        if (theUser != null && theUser.equals(username)) {
            button_edit.setVisibility(View.VISIBLE);
            button_delete.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_view_review, menu);
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
            finish();
        }

    }

    private class WebServiceDelete extends AsyncTask<Void, Void, Void> {

        int response_status;
        @Override
        protected Void doInBackground(Void... arg0) {
            try {
                // Get the information
                deleteRequestUrl(URL + id);
            } catch (IOException e) {
                // notify user of no network connection
                Context context = getApplicationContext();
                CharSequence msg = "Error: Unable to download from webservice";
                int duration = Toast.LENGTH_LONG;
                Toast toast = Toast.makeText(context, msg, duration);
                toast.show();
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);

            // notify user the sync is done
            Context context = getApplicationContext();
            CharSequence msg;
            if (response_status == 204) {
                msg = "Review has been deleted";
            } else if (response_status == 401) {
                msg = "User credentials are invalid";
            } else {
                msg = "Session timed out";
            }
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, msg, duration);
            toast.show();
        } /* onPostExecute */

        /** Given a URL, establishes a HttpUrlConnection and retrieves the content as an InputStream,
         * which it parses into the HashMap structure used to fill the ListView.
         */
        private void deleteRequestUrl(String myUrl) throws IOException {

            // retrieve from shared preferences
            SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
            final String theUser = prefs.getString("username", null);
            final String theToken = prefs.getString("usertoken", null);

            // finish up building the url
            myUrl += "?token=" + theToken;

            Log.d("deleteReview", "URL = " + myUrl);

            URL url = new URL(myUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();

            try {
                // Set Timeouts
                conn.setReadTimeout(10000);
                conn.setConnectTimeout(15000);
                conn.setRequestMethod("DELETE");
                conn.setDoInput(true);
                // Start the query
                conn.connect();
                response_status = conn.getResponseCode();

            } finally {
                // close connection
                conn.disconnect();
            }
        } /* end DownloadURL() */
    }

    public void deleteReview(View view) {
        new WebServiceDelete().execute();
        finish();
    }

    public void editReview(View view) {
        Intent intent = new Intent(this, EditReview.class);
        intent.putExtra("review_id", id);
        intent.putExtra("body", body);
        intent.putExtra("attraction", attraction);
        intent.putExtra("review_name", review_name);
        startActivityForResult(intent, 0);
    }
}