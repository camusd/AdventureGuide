package com.herokuapp.secret_bastion_27250.adventureguide;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends ActionBarActivity {

    public static final String MY_PREFS = "MyPrefsFile";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String theUser = prefs.getString("username", null);
        String theId = prefs.getString("id", null);

        Button button_login = (Button)findViewById(R.id.button);
        Button button_create_new_account = (Button)findViewById(R.id.button2);
        Button button_view_credentials = (Button)findViewById(R.id.button6);
        Button button_logout = (Button)findViewById(R.id.button3);

        if (theUser != null && !theUser.isEmpty()) {
            button_login.setVisibility(View.INVISIBLE);
            button_create_new_account.setVisibility(View.INVISIBLE);
            button_view_credentials.setVisibility(View.VISIBLE);
            button_logout.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        SharedPreferences prefs = getSharedPreferences(MY_PREFS, MODE_PRIVATE);
        String restored_userName = prefs.getString("username", null);
        String restored_userToken = prefs.getString("usertoken", null);
        String restored_userId = prefs.getString("userid", null);

        if (restored_userName != null) {
            ((MyApplication)this.getApplication()).setUserName(restored_userName);
            Log.i("username", restored_userName);
        } else {
            ((MyApplication)this.getApplication()).setUserName(null);
        }

        if (restored_userToken != null) {
            ((MyApplication)this.getApplication()).setUserToken(restored_userToken);
            Log.i("usertoken", restored_userToken);
        } else {
            ((MyApplication)this.getApplication()).setUserToken(null);
        }

        if (restored_userId != null) {
            ((MyApplication)this.getApplication()).setUserId(restored_userId);
            Log.i("userid", restored_userId);
        } else {
            ((MyApplication)this.getApplication()).setUserId(null);
        }

        return true;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 0) {
            recreate();
        }

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            // add settings stuff here
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    public void loginAccount(View view) {
        Intent intent = new Intent(this, Login.class);
        startActivityForResult(intent, 0);
    }

    public void createNewAccount(View view) {
        Intent intent = new Intent(this, CreateNewAccount.class);
        startActivity(intent);
    }

    public void logoutAccount(View view) {
        SharedPreferences.Editor editor = getSharedPreferences(MY_PREFS, MODE_PRIVATE).edit();
        editor.putString("username", "");
        editor.putString("usertoken", "");
        editor.putString("id", "");
        editor.commit();
        Context context = getApplicationContext();
        CharSequence msg = "Logout successful";
        int duration = Toast.LENGTH_LONG;
        Toast toast = Toast.makeText(context, msg, duration);
        toast.show();
        recreate();
    }

    public void viewMajorAttractions(View view) {
        Intent intent = new Intent(this, ViewMajorAttractions.class);
        startActivity(intent);
    }

    public void viewCredentials(View view) {
        Intent intent = new Intent(this, ViewCredentials.class);
        startActivity(intent);
    }
}
