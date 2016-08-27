package com.herokuapp.secret_bastion_27250.adventureguide;

import android.app.Activity;
import android.content.SharedPreferences;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;


public class ViewCredentials extends ActionBarActivity {

    public static final String MY_PREFS = "MyPrefsFile";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_credentials);

        TextView tv_user = (TextView)findViewById(R.id.adventure_guide_tv_user_name);
        TextView tv_id = (TextView)findViewById(R.id.adventure_guide_tv_id);

        // retrieve from shared preferences
        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theUser = prefs.getString("username", null);
        String theId = prefs.getString("id", null);

        // set the textviews
        tv_user.setText(theUser);
        tv_id.setText(theId);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_view_credentials, menu);
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
}
