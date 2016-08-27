package com.herokuapp.secret_bastion_27250.adventureguide;

import android.app.Application;
import android.content.SharedPreferences;

public class MyApplication extends Application {
    public static final String MY_PREFS = "MyPrefsFile";
    private String userName;
    private String userToken;
    private String userId;

    public String getUserName() {
        return userName;
    }

    public String getUserToken() {
        return userToken;
    }

    public String getUserId() { return userId; }

    public void setUserName(String name) {
        this.userName = name;
    }

    public void setUserToken(String token) {
        this.userToken = token;
    }

    public void setUserId(String id) { this.userId = id; }
}
