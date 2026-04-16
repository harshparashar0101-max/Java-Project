package com.test;

import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

public class WebcastLoginTest {

    protected WebDriver driver;

    @BeforeClass
    public void setup() {
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
    }

    @Test(priority = 1)
		public void login() throws InterruptedException {
        driver.get("https://vshowqa.on24.com/vshow/ve/");
        driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
        driver.findElement(By.xpath("//input[@name='username']")).sendKeys("Harshrole10");
        driver.findElement(By.xpath("//input[@name='password']")).sendKeys("Welcome@26");
        Thread.sleep(1000);
        driver.findElement(By.xpath("//input[@value='Login']")).click();
        Thread.sleep(2000);
        System.out.println("login successfully");
        
		}
        
		@Test ( dependsOnMethods= "login")
		public void Entershow() throws InterruptedException {
        driver.manage().timeouts().implicitlyWait(70, TimeUnit.SECONDS);
        Thread.sleep(30000);
        driver.findElement(By.xpath("//input[@id='searchInput']")).click();
        Thread.sleep(3000);
        driver.findElement(By.xpath("//input[@id='searchInput']")).sendKeys("9000379332");
        driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
        driver.findElement(By.xpath("//a[@data-row-id='9000379332']")).click();
        System.out.println("Show enter successfully");
		}

        

}
