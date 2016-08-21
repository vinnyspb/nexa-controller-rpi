//
//  InterfaceController.m
//  NexaWatchController WatchKit Extension
//
//  Created by Viacheslav Kalmykov on 2016-04-10.
//  Copyright © 2016 Viacheslav Kalmykov. All rights reserved.
//

#import "InterfaceController.h"


@interface InterfaceController()

@end


@implementation InterfaceController

- (void)awakeWithContext:(id)context {
    [super awakeWithContext:context];

    // Configure interface objects here.
    
}

- (void)willActivate {
    // This method is called when watch view controller is about to be visible to user
    [super willActivate];
}

- (void)didDeactivate {
    // This method is called when watch view controller is no longer visible
    [super didDeactivate];
}

- (IBAction)buttonOpen:(WKInterfaceButton *)sender
{
    NSLog(@"Button open Tapped!");
    [self sendToRaspberryPi:true];
}

- (IBAction)buttonClose:(WKInterfaceButton *)sender
{
    NSLog(@"Button close Tapped!");
    [self sendToRaspberryPi:false];
}

- (void)sendToRaspberryPi:(BOOL)openOrClose
{
    NSString *urlToOpen = [[NSString alloc] initWithFormat:@"http://192.168.1.117:8080/open"];
    NSString *urlToClose = [[NSString alloc] initWithFormat:@"http://192.168.1.117:8080/close"];
    
    NSURLRequest *request;
    if (openOrClose) {
        request = [NSURLRequest requestWithURL: [NSURL URLWithString:urlToOpen]];
    } else {
        request = [NSURLRequest requestWithURL: [NSURL URLWithString:urlToClose]];
    }
    
    NSURLSessionDataTask *postDataTask = [[NSURLSession sharedSession] dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        NSLog(@"Response received");
    }];
    
    [postDataTask resume];
}

@end



