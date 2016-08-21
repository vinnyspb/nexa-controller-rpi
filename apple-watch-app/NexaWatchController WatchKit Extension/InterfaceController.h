//
//  InterfaceController.h
//  NexaWatchController WatchKit Extension
//
//  Created by Viacheslav Kalmykov on 2016-04-10.
//  Copyright © 2016 Viacheslav Kalmykov. All rights reserved.
//

#import <WatchKit/WatchKit.h>
#import <Foundation/Foundation.h>

@interface InterfaceController : WKInterfaceController

- (IBAction)buttonOpen:(WKInterfaceButton *)sender;
- (IBAction)buttonClose:(WKInterfaceButton *)sender;

- (void)sendToRaspberryPi:(BOOL)openOrClose;

@end
