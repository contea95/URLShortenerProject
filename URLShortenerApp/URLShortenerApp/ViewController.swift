//
//  ViewController.swift
//  URLShortenerApp
//
//  Created by 한상혁 on 2021/10/31.
//

import UIKit


struct Url {
    let url: String
}

class ViewController: UIViewController {

    @IBOutlet var textfield: UITextField!
    @IBOutlet var result: UILabel!
    @IBOutlet var resultButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
    }

    @IBAction func ok(_ sender: Any) {
        let input_url = self.textfield.text!
        let param = "url=\(input_url)"
        let paramData = param.data(using: .utf8)
        
        // URL 객체 정의
        //let url = URL(string: "http://54.180.60.55:5000/result_json")
        let url = URL(string: "http://172.30.1.56:5000/result_json")
        // request 객체 정의
        var request = URLRequest(url: url!)
        request.httpMethod = "POST"
        request.httpBody = paramData
        
        request.addValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        request.setValue(String(paramData!.count), forHTTPHeaderField: "Content-Length")
        
        // URLSession 객체 통해 응답값 및 처리 로직 생성
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let e = error {
                NSLog("An error has occurred:: \(e.localizedDescription)")
                return
            }
            // 응답 처리 로직
            DispatchQueue.main.async() {
                do {
                    let object = try JSONSerialization.jsonObject(with: data!, options: []) as? NSDictionary
                    guard let jsonObject = object else { return }
                    
                    let result_url = jsonObject["url"] as? String
                    print(result_url!)
                    //self.result.text = "\(result_url!)"
                    self.resultButton.setTitle("54.180.60.55:5000/\(result_url!)", for: .normal)
                } catch let e as NSError {
                    print("An error has occurred while parsing JSONObject: \(e.localizedDescription)")
                }
            }
        }
        // POST 전송
        task.resume()
    }
    
    @IBAction func btnClick(_ sender: UIButton) {
        UIPasteboard.general.string = self.resultButton.currentTitle
    }
    
}
    

